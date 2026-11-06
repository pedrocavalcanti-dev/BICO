from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from apps.catalog.management.commands.seed_bico_demo import Command as SeedDemoCommand
from apps.catalog.models import ServiceListing


class ListingPublicationImageTests(SimpleTestCase):
    def test_cover_and_distinct_gallery_photo_meet_publication_minimum(self):
        listing = ServiceListing(image="catalog/listings/cover.webp")

        self.assertTrue(listing.has_minimum_publication_images(["catalog/gallery/detail.webp"]))

    def test_same_file_is_not_counted_twice(self):
        listing = ServiceListing(image="catalog/listings/cover.webp")

        self.assertFalse(listing.has_minimum_publication_images(["catalog/listings/cover.webp"]))

    def test_saved_gallery_names_are_counted(self):
        listing = ServiceListing(image="catalog/listings/cover.webp")
        listing._state.adding = False
        gallery = Mock()
        gallery.values_list.return_value = ["catalog/galleries/detail.webp"]

        with patch.object(ServiceListing, "gallery_images", gallery):
            self.assertTrue(listing.has_minimum_publication_images())


class SeedDemoImageNameTests(SimpleTestCase):
    def setUp(self):
        self.command = SeedDemoCommand()

    def test_recognizes_django_storage_collision_suffix(self):
        self.assertTrue(
            self.command._matches_storage_name("garden-trimmer_a1B2c3D.webp", "garden-trimmer.webp")
        )

    def test_does_not_match_custom_filename(self):
        self.assertFalse(
            self.command._matches_storage_name("garden-trimmer_custom.webp", "garden-trimmer.webp")
        )

    def test_preserves_custom_image_field(self):
        custom_image = SimpleNamespace(name="uploads/client-owned-image.webp")
        instance = SimpleNamespace(image=custom_image)

        changed = self.command._attach_seed_image(instance, "image", "garden-trimmer.webp")

        self.assertFalse(changed)
        self.assertEqual(instance.image.name, "uploads/client-owned-image.webp")
