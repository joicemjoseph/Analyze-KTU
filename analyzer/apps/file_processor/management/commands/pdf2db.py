import hashlib
import argparse
import os
import logging
import re

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from django.db import connection

from django.core.exceptions import MultipleObjectsReturned

from file_processor.models import *

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    
    is_supplementary_result = bool()
    semester_year = str(time.strftime("%Y")+"-"+(str(int(time.strftime("%y"))+1)))
    is_revaluation_result = bool()
    semester_number = int()
    sem = Semester()


    SUPPLEMENTARY = 'Supplementary'
    REGULAR = 'Regular'
    
    REVALUATION = 'Revaluation'
        
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
            

            text_file = settings.MEDIA_DIR+"/documents/"+os.path.basename(pdf_filename).split(".")[0]+".txt"
            os.system("pdftotext -q -layout "+pdf_filename + " " +text_file)
            # logger.info()
            
            os.system("sed -e '/^$/d' -e '/^*/d' -e '1,2 d' -e 's/\cL//' -e 's/^ *//' -e 's/ \+/ /' "+text_file+" > "+text_file.split(".")[0]+"_stripped.txt")

            fp = open(text_file.split(".")[0]+"_stripped.txt")
            institution_regex = re.compile("GOVERNMENT ENGINEERING COLLEGE, WAYANAD", re.IGNORECASE) # At present only files associated to gec wayanad
            course_regex = re.compile("(^[A-Z]{2}\d{3,6}([ ]([A-Z|\&])*)+)")
            
            student_regex = re.compile("(^([A-Z]{3,5})\d{2}([A-Z]{2})(\d{3}))")
            exam_regex = re.compile("^((Revaluation\ Result\-)?)(\ )?(B\.Tech|BTech) ((S[1-8]+)(\,?))+((\ Supplementary|\ regular|.)?) Examination \d{4}-\d{2} \((((S[1-8])(\,?)+)+) Result\)", re.IGNORECASE)
            program_regex = re.compile("^(.+)(\[(Full|Part)? Time\])$")
            
            # Lambda functions
            s = lambda line: set(re.findall("(S[1-8]+)", line))
            y = lambda line: set(re.findall("\d{4}-\d{2}", line))
            isX = lambda line, x: bool(set(re.findall("(Supplementary|Regular|Revaluation)", line)).intersection({x}))
            exam_type = lambda x, y: bool(x.intersection(y))
            p = lambda l: re.split("(\[(Full|Part)? Time\])", l)[0].lower() # program name
            ft = lambda l: bool(re.search("Part", l))
            rv = lambda l: bool(re.search("(Revaluation\ Result\-)", l)) # Revaluation result could be replaced by isX
            
            try:
                document = Document.objects.get(sha_sum=self.sha_sum_verify(pdf_filename))
                raise  CommandError("File %s already exist" % pdf_filename)
            except Document.DoesNotExist as e: 
                try:
                    document = Document.objects.create(name=pdf_filename, sha_sum=self.sha_sum_verify(pdf_filename))    
                except IntegrityError as e:
                    logger.info(e.message)
                    raise CommandError("Reached hell!")

            for line in fp:
        
                line = line.strip()
                # get course data
                if any(re.findall(institution_regex, line)):
                    institute = True
                    continue    
                elif any(re.findall(institution_regex, line)) and institute: 
                    raise CommandError("At present, Analyzer is for in-house application only")


                if exam_regex.match(line):
                    # if rv(line):
                    #     raise CommandError("Working on revaluation results")
                    
                    self.semester_name = ",".join(s(line))
                    self.semester_year = "-".join(y(line))
                    self.semester_number = int(re.findall("\d", "".join(line))[0])
                    
                    try:
                        self.sem = Semester.objects.get(number=int(re.findall("\d", "".join(line))[0]))
                    except (Semester.DoesNotExist, IntegrityError) as e:
                        raise CommandError("Please update semester using \'python manage.py semester2db\'")
                    
                    self.is_supplementary_result =  isX(line, self.SUPPLEMENTARY)
                    
                    # logger.error(self.is_supplementary_result)
                if program_regex.match(line):
                    # logger.info(p(line))
                    
                    is_full_time = ft(line)

                    if self.is_revaluation_result:
                        try:
                            semester = Semester.objects.get(number=self.semester_number) 
                            program = Program.objects.get(semester_id=semester)
                        except (Semester.DoesNotExist, Program.DoesNotExist, IntegrityError) as e:
                            raise CommandError(e.message)
                    try:
                        program, created =  Program.objects.get_or_create(name=p(line), is_full_time=ft(line), year=self.semester_year, semester_id=self.sem)
                        
                    except IntegrityError as e:
                        logger.error("some shit happened")
                    # pgm = Program.objects.get_or_create()
                if all([bool(not(re.search("college", line, re.IGNORECASE))), bool(re.match("(^[A-Za-z]{3,})+ .+(ENGG|ENGINEERING|TECHNOLOGY)$", line))]):
                    is_full_time = ft(line)
                    try:
                        program, created =  Program.objects.get_or_create(name=p(line), is_full_time=ft(line), year=self.semester_year, semester_id=self.sem)
                    except IntegrityError as e:
                        logger.error("some shit happened")
                
                if course_regex.match(line):
                    intermediate_data = line.split(" ")
                    name = intermediate_data[0]
                    code = intermediate_data[0]
                    name = str(" ".join(intermediate_data[1:]))
                    # logger.info(code + " " + name)
                    try:
                        course, created = Course.objects.get_or_create(name=name, code=code, semester_id=self.sem, program_id=program)
                        
                    except IntegrityError as e:
                        logger.error(e.message)
                        # raise CommandError("some shit happened for course")
                #get student data and loop .through it
                
                exam, created = Exam.objects.get_or_create(semester_id=self.sem, year=str(self.semester_year), document_id=document, is_supplementary_result=self.is_supplementary_result, is_revaluation_result=self.is_revaluation_result)
                if student_regex.match(line):
                    intermediate_data = line.split(" ")
                    student_reg_no = intermediate_data[0]

                    intermediate_data = "".join(intermediate_data[1:]).split(",")
                    intermediate_data = filter(None, intermediate_data)
                    student, created = Student.objects.get_or_create(reg_no=student_reg_no)
            
                    # logger.info( " " + student + " " + self.semester_year)
                    # no_change = True if re.search("Nochange", intermediate_data, re.IGNORECASE) else False # if no change in grades
                    
                    for courses_and_grades in intermediate_data:
                        course_code, grade = courses_and_grades.rsplit(")")[0].split("(") 
                        if re.search("Nochange", grade, re.IGNORECASE):
                            try:
                                exam = Exam.objects.get(semester_id=self.sem,year=str(self.semester_year), is_supplementary_result=0, is_revaluation_result=0)
                            except MultipleObjectsReturned as e:  
                                exam = exam
                            except Exam.DoesNotExist as e:
                                document.delete()
                                raise CommandError(str(e) + " ( Please insert regular exam details before revaluation.)")
                            try:
                                grade = Score.objects.get(student_id=student, year=self.semester_year, course_id=course, exam_id=exam)
                            except Score.DoesNotExist as e:
                                document.delete()
                                raise CommandError(str(e) + " ( Please insert regular exam details before revaluation.)")
                        try:
                            score, created = Score.objects.get_or_create(student_id=student, year=self.semester_year, grade=grade, course_id=course, exam_id=exam) 
                        except (Score.DoesNotExist, Course.DoesNotExist) as e:
                            raise CommandError("shits again" + str(e))

            
                # logger.info(student_reg_no+ " has awarded " + grade + " for " + course_code)
                document.save()

    def sha_sum_verify(self, fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()