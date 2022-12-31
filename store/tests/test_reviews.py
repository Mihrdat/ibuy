import pytest
from model_bakery import baker
from store.models import Product, Review
from rest_framework import status
from django.conf import settings

User = settings.AUTH_USER_MODEL


@pytest.fixture
def create_review(api_client):
    def do_create_review(product_id, data):
        return api_client.post(f'/store/products/{product_id}/reviews/', data)
    return do_create_review


@pytest.fixture
def retrieve_review(api_client):
    def do_retrieve_review(product_id, review_id):
        return api_client.get(f'/store/products/{product_id}/reviews/{review_id}/')
    return do_retrieve_review


@pytest.mark.django_db
class TestCreateReview:
    def test_if_user_is_anonymous_returns_401(self, create_review):
        product = baker.make(Product)
        data = {'description': 'a'}

        response = create_review(product.id, data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_data_is_invalid_returns_400(self, authenticate, create_review):
        product = baker.make(Product)
        user = baker.make(User)
        authenticate(user)
        data = {'description': ''}

        response = create_review(product.id, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_201(self, authenticate, create_review):
        product = baker.make(Product)
        user = baker.make(User)
        authenticate(user)
        data = {'description': 'a'}

        response = create_review(product.id, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveReview:
    def test_if_review_does_not_exists_returns_404(self, retrieve_review):
        product = baker.make(Product)

        response = retrieve_review(product.id, 0)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['detail'] == 'Not found.'

    def test_if_review_exists_returns_200(self, retrieve_review):
        product = baker.make(Product)
        user = baker.make(User)
        review = baker.make(Review, product=product, user=user)

        response = retrieve_review(product.id, review.id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == review.id
