from pydantic import BaseModel, field_validator

# class UserListRequest(BaseModel):
#     id : int
#     full_name : str
#     is_admin : bool
    
#     @field_validator("is_admin")
#     def adminVerify(cls, a):
#         if a == False:
#             raise ValueError("You need to be an admin to request user list.")
#         return a
# wrong as validation done in routers


class UserListResponse(BaseModel):
      id : int
      full_name: str
      email : str
      phone : str
      is_admin : bool
      
      class Config:
          from_attributes = True        