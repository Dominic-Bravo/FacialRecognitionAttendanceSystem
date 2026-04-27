import base64
from datetime import timedelta
from traceback import format_tb
from django import forms
from django.contrib import admin
from .models import Person, Attendance, ExcuseLetter
import base64
from django.utils.html import format_html
import base64
from django.utils.html import format_html


admin.site.site_header = "Don Jose Attendance System"        
admin.site.site_title = "Attendance System Portal"       
admin.site.index_title = "Manage Attendance & Excuses"  


def render_image_field(image_data, max_size=200):
    if not image_data:
        return "No Image"

    try:
        raw_bytes = None

        if isinstance(image_data, (bytes, bytearray, memoryview)):
            raw_bytes = bytes(image_data)

        elif isinstance(image_data, str) and image_data.strip().startswith(("iVBOR", "/9j/", "R0lGOD")):
            raw_bytes = base64.b64decode(image_data)

        elif isinstance(image_data, str) and all(c in "0123456789ABCDEFabcdef" for c in image_data[:50]):
            raw_bytes = bytes.fromhex(image_data)

        if raw_bytes:
            base64_img = base64.b64encode(raw_bytes).decode("utf-8")
            return format_html(
                '<img src="data:image/png;base64,{}" style="max-height:{}px; max-width:{}px; border:1px solid #ccc;" />',
                base64_img, max_size, max_size
            )

        return "Invalid image data"

    except Exception as e:
        return f"Error displaying image: {e}"


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "role", "position", "wage", "timestamp")
    readonly_fields = ("image_preview",)  
    search_fields = ("name", "role", "position")
    list_filter = ("role", "position")
    ordering = ("name",)

    def image_preview(self, obj):
        return render_image_field(obj.image)

    image_preview.short_description = "Profile"


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "person_name", 
        "remarks",
        "timestamp",
        "time_in_am",
        "time_out_am",
        "time_in_pm",
        "time_out_pm",
    )
    list_filter = (
        "person__role",
        "person__position",
        "remarks",
        "timestamp",
        "person",  
    )
    search_fields = ("person__name",)

    def person_name(self, obj):
        return obj.person.name if obj.person else "-"
    person_name.admin_order_field = "person__name"  
    person_name.short_description = "Person Name"



@admin.register(ExcuseLetter)
class ExcuseLetterAdmin(admin.ModelAdmin):
    list_display = ("id", "person", "reason", "start_date", "end_date", "submitted_at", "status")
    list_filter = ("status", "submitted_at", "start_date", "end_date")
    search_fields = ("person__name", "reason")
    ordering = ("-submitted_at",)

    actions = ["approve_excuses", "reject_excuses"]

    def approve_excuses(self, request, queryset):
        updated_count = 0
        for excuse in queryset:
            excuse.status = "APPROVED"
            excuse.save()
            updated_count += 1
            self._update_attendance(excuse)

        self.message_user(request, f"{updated_count} excuse(s) approved and attendance updated ✅")
    approve_excuses.short_description = "Approve selected excuse letters and update Attendance"

    def reject_excuses(self, request, queryset):
        updated = queryset.update(status="REJECTED")
        self.message_user(request, f"{updated} excuse(s) rejected ❌")
    reject_excuses.short_description = "Reject selected excuse letters"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.status == "APPROVED":
            self._update_attendance(obj)

    def _update_attendance(self, excuse):
        current_date = excuse.start_date
        while current_date <= excuse.end_date:
            attendance, created = Attendance.objects.get_or_create(
                person=excuse.person,
                timestamp__date=current_date,
                defaults={"timestamp": current_date, "remarks": "Approved Leave"}
            )

            attendance.timestamp = current_date
            attendance.time_in_am = None
            attendance.time_out_am = None
            attendance.time_in_pm = None
            attendance.time_out_pm = None
            attendance.remarks = "Approved Leave"
            attendance.save()

            current_date += timedelta(days=1)
