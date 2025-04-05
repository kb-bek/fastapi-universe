from fastapi import HTTPException, status

ExpiredTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token has expired or is invalid."
)

MissingTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Missing access token in cookies."
)

JWTErrorException = HTTPException (
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid or malformed JWT token."
)

MissingUserIDException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User ID is missing in the token payload."
)

UserNotFoundException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User not found or unauthorized."
)

UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="A user with this email already exists."
)

AuthenticationFailedException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid email or password."
)

RoomCannotBeBooked = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="This room is already booked"
)