from api.booking_client import BookingAPIClient
from api.builders import make_booking


def test_put_replaces_the_whole_booking(booking_client:BookingAPIClient, created_booking):
    booking_id, payload = created_booking
    new_payload = make_booking(firstname="Big", lastname="Boss", totalprice=222)

    r = booking_client.update_booking(booking_id, new_payload)

    assert r.status_code == 200
    assert r.json() == new_payload
    assert booking_client.get_booking(booking_id).json() == new_payload

# Payload > update_booking()

def test_update_without_token_403(api_session, created_booking):
    from api.booking_client import BookingAPIClient
    booking_id, payload = created_booking
    new_payload = make_booking(firstname="Big", lastname="Boss", totalprice=222)

    anon = BookingAPIClient(api_session)

    r = anon.update_booking(booking_id, new_payload)
    assert r.status_code == 403


def test_patch_changes_only_the_firstname(booking_client: BookingAPIClient, created_booking):
    booking_id, payload = created_booking
    patch_payload = {"firstname": "Big"}

    r = booking_client.partial_update_booking(booking_id, patch_payload)

    expected_payload = payload.copy()
    expected_payload["firstname"] = "Big"

    assert r.status_code == 200
    assert r.json() == expected_payload