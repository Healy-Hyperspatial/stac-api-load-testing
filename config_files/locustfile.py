from locust import HttpUser, task, constant, tag, run_single_user
from helpers import test_item

import os
import random
import json


class WebsiteTestUser(HttpUser):
    # If one declares a host attribute in the user class, it will be used in the
    # case when no --host is specified on the command line or in the web request.
    host = os.getenv("LOCUST_HOST", "http://localhost:8083")
    default_load_multiplier = 1

    def on_start(self):
        """Called when a Locust start before any task is scheduled."""
        pass

    def on_stop(self):
        """Called when the TaskSet is stopping."""
        pass

    def load_file(self, file) -> dict:
        f = open(file)
        data = json.load(f)
        return data

    def get_collection_ids(self):
        """Get all Collection IDs."""
        collections_response = self.client.get("/collections", name="get-collections")
        collections_body = collections_response.json()
        collection_ids = [
            collection["id"] for collection in collections_body["collections"]
        ]
        return collection_ids

    def parse_request_items(self, collection_id, items_response):
        """Parse response, if > 0 items then request Items."""
        items_body = items_response.json()
        item_ids = [feature["id"] for feature in items_body["features"]]

        # Request between 1 and min(10, result count) Items, serially
        for item_id in item_ids:
            self.client.get(
                f"/collections/{collection_id}/items/{item_id}", name="get-item"
            )

    def get_collection_bbox(self, collection_id):
        """get the bbox of a collection"""
        collection_response = self.client.get(
            f"/collections/{collection_id}", name="get-collection"
        )
        return collection_response.json()["extent"]["spatial"]["bbox"][0]

    def get_sortby(self, get_post):
        """Randomize the sort order among available fields."""
        # TODO retrieve all sortable fields common to items in collection
        fields = ["id", "properties.datetime", "properties.eo:cloud_cover"]
        directions = [random.choice(["+", "-"]) for _ in fields]
        sym2text = {"+": "asc", "-": "desc"}

        if get_post == "GET":
            return [
                f"{direction}{field}" for direction, field in zip(directions, fields)
            ]
        elif get_post == "POST":
            return [
                {"field": field, "direction": sym2text[direction]}
                for field, direction in zip(fields, directions)
            ]

    @tag("root_catalog")
    @task(default_load_multiplier)
    def get_root_catalog(self):
        self.client.get("/", name="get-landing")

    @tag("all_collections")
    @task(default_load_multiplier)
    def get_all_collections(self):
        self.client.get("/collections", name="get-collections")

    @tag("get_collection")
    @task(default_load_multiplier)
    def get_collection(self):
        self.client.get("/collections/test-collection", name="get-collection")

    @tag("item_collection")
    @task(default_load_multiplier)
    def get_item_collection(self):
        self.client.get("/collections/test-collection/items", name="get-items")

    @tag("get_item")
    @task(default_load_multiplier)
    def get_item(self):
        random_number = random.randint(1, 11)
        item = self.load_file("data_loader/setup_data/sentinel-s2-l2a-cogs_0_100.json")
        random_id = item["features"][random_number]["id"]
        self.client.get(
            f"/collections/test-collection/items/{random_id}", name="get-item"
        )

    @tag("get_bbox")
    @task(0)
    def get_bbox_search(self):
        self.client.get(
            "/search?bbox=-16.171875,-79.095963,179.992188,19.824820",
            name="get-search-bbox",
        )

    @tag("post_bbox")
    @task(default_load_multiplier)
    def post_bbox_search(self):
        self.client.post(
            "/search",
            json={"bbox": [16.171875, -79.095963, 179.992188, 19.824820]},
            name="post-search-bbox",
        )

    @tag("point_intersects")
    @task(default_load_multiplier)
    def post_intersects_search(self):
        self.client.post(
            "/search",
            json={
                "collections": ["test-collection"],
                "intersects": {"type": "Point", "coordinates": [150.04, -33.14]},
            },
            name="post-search-intersects",
        )

    @tag("basic_nonspatial")
    @task(default_load_multiplier)
    def basic_nonspatial_search(self):
        """Simulate a user searching for a Collection by ID."""
        collection_ids = self.get_collection_ids()
        collection_id = random.choice(collection_ids)

        # Randomize GET / POST
        get_post = random.choice(["GET", "POST"])
        if get_post == "GET":
            items_response = self.client.get(
                f"/search?collections={collection_id}", name="get-search-collection"
            )
        elif get_post == "POST":
            items_response = self.client.post(
                "/search",
                json={"collections": [collection_id]},
                name="post-search-collection",
            )

        self.parse_request_items(collection_id, items_response)

    @tag("intersects_sortby")
    @task(default_load_multiplier)
    def paged_poi_search(self):
        """Simulate a user seaching within a collection bbox using a point."""
        # Get the bbox of a random collection
        collection_ids = self.get_collection_ids()
        collection_id = random.choice(collection_ids)
        bbox = self.get_collection_bbox(collection_id)

        # Create random point inside bbox for /search intersects
        x = random.random() * (bbox[2] - bbox[0]) + bbox[0]
        y = random.random() * (bbox[3] - bbox[1]) + bbox[1]

        # Search (only POST possible for "intersects")
        sortby = self.get_sortby("POST")
        items_response = self.client.post(
            "/search",
            json={
                "collections": [collection_id],
                "intersects": {"type": "Point", "coordinates": [x, y]},
                "sortby": sortby,
            },
            name="post-multisearch-intersects",
        )

        self.parse_request_items(collection_id, items_response)

    @tag("user_bbox")
    @task(default_load_multiplier)
    def paged_bbox_search(self):
        """Simulate a user searching within a collection bbox using an AOI."""
        # Get the bbox of a random collection
        collection_ids = self.get_collection_ids()
        collection_id = random.choice(collection_ids)
        bbox = self.get_collection_bbox(collection_id)

        # Create a random search bbox inside collection bbox
        x = [random.random() * (bbox[2] - bbox[0]) + bbox[0] for _ in range(2)]
        y = [random.random() * (bbox[3] - bbox[1]) + bbox[1] for _ in range(2)]
        search_bbox = [min(x), min(y), max(x), max(y)]

        # Search, randomly using GET or POST
        get_post = random.choice(["GET", "POST"])
        sortby = self.get_sortby(get_post)
        if get_post == "GET":
            search_bbox_str = ",".join([str(x) for x in search_bbox])
            items_response = self.client.get(
                f"/search?collections={collection_id}&bbox={search_bbox_str}"
                + f"&sortby={','.join(sortby)}",
                name="get-multisearch-bbox",
            )
        elif get_post == "POST":
            items_response = self.client.post(
                "/search",
                json={
                    "collections": [collection_id],
                    "bbox": search_bbox,
                    "sortby": sortby,
                },
                name="post-multisearch-bbox",
            )

        self.parse_request_items(collection_id, items_response)

    #### CRUD routes
    @tag("create_item")
    @task(0)
    def create_item(self):
        random_number = random.randint(1, 100000)
        item = test_item
        item["id"] = f"test-item-{random_number}"
        item["collection"] = "test-collection"
        self.client.post(
            "/collections/test-collection/items", json=item, name="post-create-item"
        )


# Run tests in debugger if launched directly,
# e.g. "python3 debugging.py", not "locust -f debugging.py"
if __name__ == "__main__":
    run_single_user(WebsiteTestUser)
