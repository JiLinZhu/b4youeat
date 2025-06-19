"""
Quick interactive test for ReviewService gRPC endpoints.

Make sure the compose stack is running first:
    docker compose up -d

Then simply run:
    python scripts/test_reviews_grpc.py
"""
import asyncio
import datetime
from b4youeat.lib.proto_converters import datetime_to_timestamp
import grpc
from proto.services import review_service_pb2, review_service_pb2_grpc


GRPC_ENDPOINT = "localhost:50051"


async def main() -> None:
    async with grpc.aio.insecure_channel(GRPC_ENDPOINT) as channel:
        stub = review_service_pb2_grpc.ReviewServiceStub(channel)

        create_resp = await stub.CreateReview(
            review_service_pb2.CreateReviewRequest(
                restaurant_id=1,
                user_id=1,
                content="Automated smoke-test review",
                visit_date=datetime_to_timestamp(datetime.datetime.now(datetime.timezone.utc)),
                rating=4,
            )
        )
        print("Created Review →", create_resp.review)

        get_resp = await stub.GetReview(
            review_service_pb2.GetReviewRequest(id=create_resp.review.id)
        )
        print("Fetched  Review →", get_resp.review)


if __name__ == "__main__":
    asyncio.run(main())
