import hashlib
import argparse
import os
import logging
import re

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from file_processor.models import *

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    args = '<ktu result file>'
    help = 'given pdf result file is updated to the database'

    def add_arguments(self, parser):
        # parser.add_argument('poll_id', nargs='+', type=str)
        parser.add_argument('--pdf', action='store_true',
            help='put pdf file provided by ktu')

        # this collects the unrecognized arguments to pass through to webassets
        parser.add_argument('args', nargs=argparse.REMAINDER)

    def handle(self, *args, **options):
        if len(args) != 0:
            file_name = args
            logger.info(file_name)            
            self.processFile(file_name)
    def processFile(self, f):
        for pdf_filename in f:
            
            # Save file meta to db
            try:
                document = Document.objects.create(name=pdf_filename, sha_sum=self.sha_sum_verify(pdf_filename))    
            except IntegrityError as e:
                logger.info(e.message)
                raise  CommandError("File %s already exist" % pdf_filename)

            text_file = settings.MEDIA_DIR+"/documents/"+os.path.basename(pdf_filename).split(".")[0]+".txt"
            os.system("pdftotext -q -layout "+pdf_filename + " " +text_file)
            # logger.info()
            
            os.system("sed -e '/^$/d' -e '/^*/d' -e '1,2 d' -e 's/\cL//' -e 's/^ *//' -e 's/ \+/ /' "+text_file+" > "+text_file.split(".")[0]+"_stripped.txt")
            fp = open(text_file.split(".")[0]+"_stripped.txt")
            
            course_regex = re.compile("(^[A-Z]{2}\d{3,6}([ ]([A-Z])*)+)")
            student_regex = re.compile("(^([A-Z]{3,5})\d{2}([A-Z]{2})(\d{3}))")
            institution_regex = re.compile("^Exam Centre:")
            exam_regex = re.compile("^B.Tech (S[1-8],?)+ (Supplementary|Regular) Examination \d{4}-\d{2} \((S[1-8],?)+ Result\)")
            program_regex = re.compile("^(.+)(\[(Full|Part)? Time\])$")
            
            # Lambda functions
            s = lambda line: set(re.findall("(S[1-8]+)", line))
            y = lambda line: set(re.findall("\d{4}-\d{2}", line))
            isSupplementary = lambda line: bool(set(re.findall("(Supplementary|Regular)", line)).intersection({'Supplementary'}))
            exam_type = lambda x, y: bool(x.intersection(y))
            p = lambda l: re.split("(\[(Full|Part)? Time\])", l)[0].lower() # program name
            ft = lambda l: bool(set(re.split("(\[(Full|Part)? Time\])", l)[1]).intersection(set('Full')))
            
            # Global loop variables

            for line in fp:
                line = line.strip()

                # get course data
                if exam_regex.match(line):
                    name = line
                    
                    semester_name = ",".join(s(line))
                    semester_year = "-".join(y(line))
                    
                    sem = Semester.objects.get(number=int(re.findall("\d", "".join(line))[0]))
        
                    document.is_supplementary_result =  isSupplementary(line)
                    # document.save()
                
                if program_regex.match(line):
                    # logger.info(p(line))
                    
                    is_full_time = ft(line)

                    try:
                        program, created =  Program.objects.get_or_create(name=p(line), is_full_time=ft(line), year=semester_year, semester_id=sem)
                        # logger.info()
                    except IntegrityError as e:
                        logger.info("some shit happened")
                    # pgm = Program.objects.get_or_create()
                
                if course_regex.match(line):
                    intermediate_data = line.split(" ")
                    name = intermediate_data[0]
                    code = intermediate_data[0]
                    name = str(" ".join(intermediate_data[1:]))
                    # logger.info(code + " " + name)
                    try:
                        course, created = Course.objects.get_or_create(name=name, code=code, semester_id=sem, program_id=program)
                    except IntegrityError as e:
                        logger.info("some shit happened for course " + str(course))
                #get student data and loop through it
                if student_regex.match(line):
                    intermediate_data = line.split(" ")
                    student_reg_no = intermediate_data[0]
                    student, created = Student.objects.get_or_create(reg_no=student_reg_no)
                    for courses_and_grades in intermediate_data[1:]:
                        course_code, grade = courses_and_grades.rsplit(")")[0].split("(")
                        score, created = Score.objects.get_or_create(student_id=student, year=semester_year, grade=grade, course_id=Course.objects.get(code=course_code)) 
                        # logger.info(student_reg_no+ " has awarded " + grade + " for " + course_code)

    def sha_sum_verify(self, fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()