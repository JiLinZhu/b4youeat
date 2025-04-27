import asyncio
import logging
import grpc
from grpc import aio

from db import init_db, async_session
from models import models

from proto.services import review_service_pb2_grpc, review_service_pb2
from proto.data import review_pb2

class ReviewService(review_service_pb2_grpc.ReviewServiceServicer):
    async def CreateReview(
        self,
        request: review_service_pb2.CreateReviewRequest,
        context: grpc.aio.ServicerContext,      
    ) -> review_service_pb2.CreateReviewResponse:       
        async with async_session() as session:
            review = models.Review(
                restaurant_id=request.restaurant_id,
                user_id=request.user_id,
                content=request.content,
                rating=request.rating,
            )
            session.add(review)
            await session.commit()
            await session.refresh(review)

            return review_service_pb2.CreateReviewResponse(
                review=review_pb2.Review(
                    id=review.id,
                    restaurant_id=review.restaurant_id,
                    user_id=review.user_id,
                    content=review.content,
                    rating=review.rating,
                    date=str(review.date),
                )
            )

    async def GetReview(
        self,
        request: review_service_pb2.GetReviewRequest,
        context: grpc.aio.ServicerContext,
    ) -> review_service_pb2.GetReviewResponse:
        async with async_session() as session:
            result = await session.get(models.Review, request.id)
            if not result:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Review not found")
                return review_service_pb2.Review()
            return review_service_pb2.GetReviewResponse(
                review=review_service_pb2.Review(
                    id=result.id,
                    restaurant_id=result.restaurant_id,
                    user_id=result.user_id,
                    content=result.content,
                    rating=result.rating,
                    date=str(result.date),
                )
            )

async def serve() -> None:
    await init_db()

    server = aio.server()
    review_service_pb2_grpc.add_ReviewServiceServicer_to_server(ReviewService(), server)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)

    logging.info("🚀 gRPC server listening on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s %(message)s")
    try:
        asyncio.run(serve())
    except KeyboardInterrupt:
        logging.info("Server interrupted, shutting down…")
