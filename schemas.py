"""
Phần 1: Thiết kế cơ sở dữ liệu và Phân tích quan hệSơ đồ thực thể liên kết (ERD)Student (1) ──── (N) Registration (N) ──── (1) Workshop
students (1) — (N) registrations qua registrations.student_id
workshops (1) — (N) registrations qua registrations.workshop_id
Mỗi dòng Registration = 1 lượt đăng ký cụ thể (student_id, workshop_id, registered_at)
Xác định vị trí khóa ngoạiRegistration là bảng con (Child Table) bắt buộc giữ cả 2 khóa ngoại (student_id, workshop_id), vì:

Không thể đặt FK ở Student hoặc Workshop — mỗi bản ghi ở 2 bảng này có thể tham gia nhiều lượt đăng ký khác nhau, một cột FK đơn không lưu được nhiều giá trị.
Registration đóng vai trò "bảng phụ thuộc" — nó không tồn tại độc lập, chỉ có ý nghĩa khi gắn với 1 sinh viên và 1 workshop cụ thể → đúng bản chất child table trong quan hệ N-N.
Đặt FK tại đây giúp DB tự động từ chối các bản ghi đăng ký rác (student_id/workshop_id không tồn tại) nhờ ràng buộc ForeignKey ở cấp database, giải quyết đúng vấn đề "dữ liệu rác" nêu ở bối cảnh bài toán.
Phân tích đánh đổi: secondary vs 2 quan hệ 1-N riêng biệt Khía cạnhDùng secondaryDùng 2 quan hệ 1-NTruy xuấtstudent.workshops trả list trực tiếp, không cần vòng lặpPhải duyệt [r.workshop for r in student.registrations]Truy cập cột phụ (registered_at)Không truy cập được trực tiếp qua student.workshops (list chỉ chứa Workshop, mất thông tin thời gian đăng ký)Truy cập được dễ dàng qua registration.registered_atĐộ phức tạp codeÍt relationship hơn, gọnNhiều relationship hơn, tường minh từng bước Phù hợp khi nàoBảng trung gian chỉ có 2 FK thuần, không có dữ liệu bổ sung cần dùng thường xuyênBảng trung gian có thêm cột nghiệp vụ quan trọng (như registered_at)Với bài này, đề bài yêu cầu bắt buộc dùng secondary để đáp ứng đúng output ở mục 5 (student.workshops, workshop.students), nên source code bên dưới cấu hình theo hướng này. Cột registered_at vẫn được lưu đầy đủ trong bảng registrations, chỉ là không lấy trực tiếp qua student.workshops — nếu cần truy vấn kèm thời gian đăng ký thì query trực tiếp bảng Registration.
"""

from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict


class RegistrationCreate(BaseModel):
    student_id: int
    workshop_id: int


class WorkshopBrief(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str


class StudentBrief(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str


class StudentWorkshopsOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    student_id: int
    full_name: str
    workshops: List[WorkshopBrief]


class WorkshopStudentsOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    workshop_id: int
    title: str
    students: List[StudentBrief]


class RegistrationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int
    workshop_id: int
    registered_at: datetime