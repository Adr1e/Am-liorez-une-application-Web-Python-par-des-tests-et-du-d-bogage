from locust import HttpUser, task, between

class GudlftUser(HttpUser):
    # Wait time between tasks to simulate think-time
    wait_time = between(0.5, 1.5)

    @task(3)
    def home(self):
        # Basic read: should be fast and stable
        self.client.get("/")

    @task(1)
    def book_one_place(self):
        # Login then attempt a simple booking
        # Note: this flow assumes the test data allows a booking of 1
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})
        self.client.post("/purchasePlaces", data={
            "club": "Simply Lift",
            "competition": "Spring Festival",
            "places": "1",
        })
