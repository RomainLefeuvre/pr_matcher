import csv
from github import Github
import argparse
from typing import List, Optional
from unidecode import unidecode

class Student:
    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name
        self.pull_request: Optional[str] = None
    
    def assign_pull_request(self, pull_request: str):
        self.pull_request = pull_request
    
    def __repr__(self):
        return f"Student('{self.first_name}', '{self.last_name}')"

class PullRequestMatcher:
    pull_request = []
    students : List[Student] = []
    out_csv : str
    repo : str

    def __init__(self,csv_path : str, repo : str):
        self.out_csv = csv_path.replace('.csv',repo.replace("/","_")+'_result.csv')
        self.repo = repo
        self.init_student_list_from_csv(csv_path)
        self.fetch_pull_requests()
        

    def init_student_list_from_csv(self, csv_file: str) :
        student_list: List[Student] = []
        with open(csv_file, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                last_name, first_name = row
                student = Student(first_name, last_name)
                student_list.append(student)
        self.students=student_list


    def fetch_pull_requests(self):
        g = Github()
        repo = g.get_repo(self.repo)
        self.pull_request = repo.get_pulls(state='open')  # Fetch open pull requests

    def isUniqueLastName(self, current_student : Student) -> bool:
        alreadyMatch = False
        for student in self.students:
            if current_student.last_name in student.last_name :
                if alreadyMatch:
                    return False
                else:
                    alreadyMatch=True
        return True

    def isUniqueFirstName(self, current_student : Student) -> bool:
        alreadyMatch = False
        for student in self.students:
            if current_student.first_name in student.first_name:
                if alreadyMatch:
                    return False
                else:
                    alreadyMatch=True
        return True
            
    def findAndAddStudentPR(self,student : Student):
        pull_request_matching = []
        pull_request_matching_last_name = []
        pull_request_matching_first_name = []
        unique_first_name = self.isUniqueFirstName(student)
        unique_last_name = self.isUniqueLastName(student)
        for pr in self.pull_request:
            title = self.normalize(pr.title)
            if self.normalize(student.last_name) in title and self.normalize(student.first_name) in title:
                pull_request_matching.append(pr)
            if self.normalize(student.last_name) in title and unique_last_name:
                pull_request_matching_last_name.append(pr)
            if self.normalize(student.first_name) in title and unique_first_name:
                pull_request_matching_first_name.append(pr)

        if len(pull_request_matching)==1:
            student.assign_pull_request(pull_request_matching[0].html_url)
        elif len(pull_request_matching)>1:
            print("error for "+student.first_name+" "+student.last_name)
        elif len(pull_request_matching_last_name)==1:
            student.assign_pull_request(pull_request_matching_last_name[0].html_url)
            print("Matched by last name "+student.first_name+" "+student.last_name)
        elif len(pull_request_matching_first_name)==1:
            student.assign_pull_request(pull_request_matching_first_name[0].html_url)
            print("Matched by first name "+student.first_name+" "+student.last_name)
        else :
            print("Not Found "+student.first_name+" "+student.last_name+" "+str(len(pull_request_matching))+" "+str(len(pull_request_matching_last_name))+" "+str(len(pull_request_matching_first_name))+" unique first name : "+str(unique_first_name)+" unique last name "+str(unique_last_name))

    def normalize(self, string:str):
        return unidecode(string).lower()
        
    def match(self):
        for student in self.students:
            self.findAndAddStudentPR(student)

    def export_to_csv(self):
        with open(self.out_csv, 'w', newline='') as file:
            writer = csv.writer(file)
            for student in self.students:
                writer.writerow([student.last_name,student.first_name,student.pull_request])
    def print_unafected_pr(self):
        missing_pr = [pr for pr in self.pull_request if len([student for student in self.students if pr.html_url == student.pull_request])==0 ]
        for pr in missing_pr :
            print("Unnafected pr : "+pr.html_url+" "+pr.title)
    def print_affected_to_one_student_pr(self):
        missing_pr = [pr for pr in self.pull_request if len([student for student in self.students if pr.html_url == student.pull_request])<=1 ]
        for pr in missing_pr :
            print("check this affected to less than two student pr : "+pr.html_url+" "+pr.title)
    def print_affected_to_more_than_two_student_pr(self):
        missing_pr = [pr for pr in self.pull_request if len([student for student in self.students if pr.html_url == student.pull_request])>2 ]
        for pr in missing_pr :
            print("check this affected to more than two student pr : "+pr.html_url+" "+pr.title)

def main(args):
    matcher :PullRequestMatcher = PullRequestMatcher(args.csv_path,args.repo)
    matcher.match()
    matcher.export_to_csv()
    matcher.print_unafected_pr()
    matcher.print_affected_to_one_student_pr()
    matcher.print_affected_to_more_than_two_student_pr()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch GitHub pull requests containing first name and last name from a CSV file and save the results to a new CSV file.')
    parser.add_argument('csv_path', type=str, help='Path to the CSV file containing first names and last names.')
    parser.add_argument('repo', type=str, help='GitHub repository.')
    args = parser.parse_args()
    main(args)
