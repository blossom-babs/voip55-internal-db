from pymodm import connect, MongoModel, fields, EmbeddedMongoModel
from pymongo.write_concern import WriteConcern
from flask_login import UserMixin
from datetime import datetime
from flask_login import current_user
import settings

print(settings.mongodb_url)
connect(settings.mongodb_url)



class Staff(UserMixin, MongoModel):
    full_name = fields.CharField(required=True, blank=False)
    job_position = fields.CharField(required=True, blank=False)
    email = fields.EmailField(required=True, blank=False)
    password = fields.CharField(required=True, blank=False)
    admin = fields.BooleanField(default=False)
    confirm_user = fields.BooleanField(default=False)
    approval_status = fields.CharField(required=True, blank=False, default="pending")

    class Meta:
        write_concern = WriteConcern(j=True)
        ignore_unknown_fields = True

    def get_id(self):
        return str(self.pk)


class Service(EmbeddedMongoModel):
    name = fields.CharField(required=False, blank=True)
    contract = fields.CharField(required=False, blank=True)
    payg = fields.CharField(required=False, blank=True)


class Password(EmbeddedMongoModel):
    option_1 = fields.CharField(required=False, blank=True)
    option_2 = fields.CharField(required=False, blank=True)
    other_options = fields.CharField(required=False, blank=True)
    description = fields.CharField(required=False, blank=True)
    file_upload = fields.CharField(required=False, blank=True)


class Helpdesk(EmbeddedMongoModel):
    date = fields.DateTimeField(required=False, blank=True)
    staff_on_duty = fields.CharField(required=False, blank=True)
    service_request = fields.CharField(required=False, blank=True)


class OfficeDevices (EmbeddedMongoModel):
    device = fields.CharField(required=False, blank=True)
    username = fields.CharField(required=False, blank=True)
    password = fields.CharField(required=False, blank=True)
    configuration = fields.CharField(required=False, blank=True)


class Clients(MongoModel):
    client_name = fields.CharField(required=False, blank=True)
    address = fields.CharField(required=False, blank=True)
    email = fields.EmailField(required=False, blank=True)
    customer_ref = fields.CharField(required=False, blank=True)
    telephone_num1 = fields.CharField(required=False, blank=True)
    telephone_num2 = fields.CharField(required=False, blank=True)
    telephone_num3 = fields.CharField(required=False, blank=True)
    business_name = fields.CharField(required=False, blank=True)
    services = fields.EmbeddedDocumentListField(Service, required=False, blank=True, default=[])
    passwords = fields.EmbeddedDocumentListField(Password, required=False, blank=True, default=[])
    helpdesk = fields.EmbeddedDocumentListField(Helpdesk, required=False, blank=True, default=[])
    officeDevices = fields.EmbeddedDocumentListField(OfficeDevices, required=False, blank=True, default=[])
    isDeleted = fields.BooleanField(default=False)
    date_created = fields.DateTimeField(default=datetime.now())
    staff_created = fields.CharField(required=False, blank=True)
    display = fields.BooleanField(default=True)

    class Meta:
        write_concern = WriteConcern(j=True)
        ignore_unknown_fields = True


class Reports(MongoModel):
    reportsTitle = fields.CharField(required=False, blank=True)
    reportsMessage = fields.CharField(required=False, blank=True)
    currentDate = fields.DateTimeField(default=datetime.now())


class Tasks(MongoModel):
    staff__ = fields.CharField(required=False, blank=True)
    tasks = fields.CharField(required=False, blank=True)
    tasksMessage = fields.CharField(required=False, blank=True)


class SupplyInfo (EmbeddedMongoModel):
    typeOfService = fields.CharField(required=False, blank=True)
    paymentRef = fields.CharField(required=False, blank=True)
    paymentAmt = fields.CharField(required=False, blank=True)
    customer = fields.CharField(required=False, blank=True)
    expiryDate = fields.CharField(required=False, blank=True)
    comment = fields.CharField(required=False, blank=True)


class Suppliers(MongoModel):
    supplierName = fields.CharField(required=False, blank=True)
    supplierAddress = fields.CharField(required=False, blank=True)
    supplierContacts = fields.CharField(required=False, blank=True)
    supplierEmail = fields.CharField(required=False, blank=True)
    supply_info = fields.EmbeddedDocumentListField(SupplyInfo, required=False, blank=True, default=[])
    isDeleted = fields.BooleanField(default=False)
    date_created = fields.DateTimeField(default=datetime.now())
    staff_created = fields.CharField(required=False, blank=True)
    display = fields.BooleanField(default=True)
    
    class Meta:
        write_concern = WriteConcern(j=True)
        ignore_unknown_fields = True
    
    # last_updated = fields.DateTimeField(default=datetime.now())
    