from config import cursor, db

class Billing:
    def __init__(self, reservation_id, customer_id):
        self.reservation_id = reservation_id
        self.customer_id = customer_id

    def fetch_bill(self):
        query = """
        SELECT totalAmount, taxes, discounts, paymentStatus
        FROM billing
        WHERE reservationId = %s
        """
        cursor.execute(query, (self.reservation_id,))
        return cursor.fetchone()

    def update_payment_status(self, status):
        query = """
        UPDATE billing
        SET paymentStatus = %s
        WHERE reservationId = %s
        """
        cursor.execute(query, (status, self.reservation_id))
        db.commit()

    def generate_bill_summary(self):
        bill = self.fetch_bill()
        if bill:
            total, taxes, discounts, payment_status = bill
            return f"Bill Summary:\nTotal: ${total}\nTaxes: ${taxes}\nDiscounts: ${discounts}\nStatus: {payment_status}"
        return "No billing details found."
