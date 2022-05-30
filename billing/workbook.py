from xlwt import Workbook, easyxf, Formula


class ReportBook(Workbook):
    h_bold_center = easyxf("align: vert centre, horiz centre;font: bold 1,height 280;")
    bold_center = easyxf("align: vert centre, horiz centre;font: bold 1;")
    bold_left = easyxf("align: vert centre, horiz left;font: bold 1;")
    bold = easyxf("font: bold 1;")
    middle_width = 256 * 20
    short_width = 256 * 5
    long_width = 256 * 43
    tall_height = 600

    def add_group(self, title: str, sheetname: str):
        worksheet = self.add_sheet(sheetname)
        # style
        worksheet.col(0).width = self.short_width
        worksheet.col(1).width = self.long_width
        worksheet.col(2).width = self.middle_width
        worksheet.col(3).width = self.middle_width
        worksheet.col(4).width = self.middle_width
        worksheet.row(0).height = self.tall_height
        # header
        worksheet.write_merge(0, 0, 2, 4, title, self.h_bold_center)
        worksheet.write(1, 0, "№", self.bold_left)
        worksheet.write(1, 1, "Student", self.bold_center)
        worksheet.write(1, 2, "Expected", self.bold_center)
        worksheet.write(1, 3, "Paid", self.bold_center)
        worksheet.write(1, 4, "Delta", self.bold_center)
        return worksheet

    def add_headsheet(self, title: str, sheetname='Report'):
        worksheet = self.add_sheet(sheetname)
        # style
        worksheet.col(0).width = self.middle_width
        worksheet.col(1).width = self.middle_width
        worksheet.col(2).width = self.middle_width
        worksheet.col(3).width = self.middle_width
        worksheet.col(4).width = self.middle_width
        worksheet.row(0).height = self.tall_height
        # header
        worksheet.write_merge(0, 0, 1, 3, title, self.h_bold_center)
        worksheet.write(1, 0, "Total Groups", self.bold_center)
        worksheet.write(1, 1, "Total Students", self.bold_center)
        worksheet.write(1, 2, "Total Income", self.bold_center)
        worksheet.write(1, 3, "Total Debt", self.bold_center)
        worksheet.write(1, 4, "Delta", self.bold_center)
        worksheet.write(2, 4, Formula(f"C3-D3"))
        return worksheet
