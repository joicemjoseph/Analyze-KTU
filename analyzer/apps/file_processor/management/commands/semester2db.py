import hashlib
import argparse
import os
import logging
import re
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from file_processor.models import Semester

logger = logging.getLogger(__name__)

class Command(BaseCommand):
	NAME = {
		1 : "One", 
		2 : "Two",
		3 : "Three",
		4 : "Four",
		5 : "Five",
		6 : "Six",
		7 : "Seven",
		8 : "Eight",
	}
	def handle(self, *args, **options):
		for semester in range(1,9):
			Semester.objects.get_or_create(number=semester, name=self.NAME[semester], minimum_credit=20)