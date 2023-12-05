from django.test import TestCase, Client
from shop.models import Purchase, Product
from shop.views import PurchaseCreate, check_buys_count


class PurchaseCreateTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_webpage_accessibility(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_create_new_purchase(self):
        # response = self.client.post("/buy/3/", {'person': 'test_person', 'address': 'test_address'})
        # purchase_list = Purchase.objects.all()
        # for purchase in purchase_list:
        #     print(f"{purchase.product.name} {purchase.person} {purchase.product.price}")
        # self.assertEqual(response.status_code, 200)

        pass

class PriceRisingTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_price_rising(self):
        product = Product.objects.create(name="book", price=100)
        for _ in range(10):
            Purchase.objects.create(product=product,
                                    person="Ivanov",
                                    address="Svetlaya St.")
        check_buys_count()
        self.assertAlmostEqual(Product.objects.get(name="book").price,
                               product.price + product.price * 0.15,
                               delta=0.01)
