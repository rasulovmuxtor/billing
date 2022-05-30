import os
from django.db.models import F, Sum
from django.utils import timezone
from django.conf import settings
from xlwt import Formula
from .workbook import ReportBook
from organization.models import Organization, Group
from student.models import Student, Transaction
from billing.models import Report, StudentReport


class OrganizationReportCreator:
    @staticmethod
    def run():
        todaystr = timezone.now().strftime("%Y-%B-%d")
        organizations = Organization.objects.filter(groups__isnull=False).distinct()
        student_reports = []
        updated_students = []
        updated_organizations = []
        reports = []
        for organization in organizations:
            income = Transaction.objects.filter(student__group__organization=organization, type__gt=0).aggregate(
                Sum('amount')).get('amount__sum') or 0
            organization.balance += income
            updated_organizations.append(organization)
            report = Report(organization=organization, total_income=income)
            reports.append(report)
            groups = Group.objects.filter(organization=organization).annotate(tariff_price=F('tariff__price'))
            report.total_groups = len(groups)

            workbook = ReportBook()
            headsheet = workbook.add_headsheet(f"{organization.title} {todaystr}")

            for group in groups:
                worksheet = workbook.add_group(f"{group.title} {todaystr}", f"#{group.id} {group.title}")

                students = Student.objects.filter(group=group).annotate(tariff_price=F('tariff__price'))
                report.total_students += len(students)
                row = 2
                for student in students:
                    if student.tariff_price is None:
                        price = group.tariff_price
                    else:
                        price = student.tariff_price
                    student.balance -= price
                    if student.balance > 0:
                        report.overpayment += student.balance
                    else:
                        report.debt += student.balance
                    student_report = StudentReport(organization_id=organization.id, expected=price,
                                                   delta=student.balance, student_id=student.id)
                    student_reports.append(student_report)
                    updated_students.append(student)
                    worksheet.write(row, 0, row - 1)
                    worksheet.write(row, 1, student.full_name)
                    worksheet.write(row, 2, student_report.expected)
                    worksheet.write(row, 3, student_report.delta)
                    row += 1
                    worksheet.write(row - 1, 4, Formula(f"D{row}-C{row}"))
                worksheet.write(row, 1, "Total:", workbook.bold_left)
                worksheet.write(row, 2, Formula(f"SUM(C3:C{row - 1})"), workbook.bold)
                worksheet.write(row, 3, Formula(f"SUM(D3:D{row - 1})"), workbook.bold)
                worksheet.write(row, 4, Formula(f"SUM(E3:E{row - 1})"), workbook.bold)
            headsheet.write(2, 0, report.total_groups)
            headsheet.write(2, 1, report.total_students)
            headsheet.write(2, 2, report.total_income)
            headsheet.write(2, 3, report.debt)

            filename = f"{todaystr}.xls"
            mediapath = f"reports/{organization.title}"
            directory = f"{settings.MEDIA_ROOT}/{mediapath}"
            file_dir_exists = os.path.exists(directory)
            if not file_dir_exists:
                os.makedirs(directory)
            filepath = os.path.join(directory, filename)
            workbook.save(filepath)
            report.excel.name = f"{mediapath}/{filename}"
        Organization.objects.bulk_update(updated_organizations, ['balance'])
        StudentReport.objects.bulk_create(student_reports, 1000)
        Student.objects.bulk_update(updated_students, ['balance'])
        Report.objects.bulk_create(reports, 1000)
