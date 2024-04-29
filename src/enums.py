import enum

class TaskState(enum.Enum):
    Wait = "Ожидает"
    Accepted = "Выполняется"
    Done = "Завершена"
    Rejected = "Отклонена"