# 5.1: A lecturer is an employee while holding that role, but the role is not a
# permanent identity. Promotion changes pay/responsibilities, not the employee.
# 5.2-3: Employee delegates pay to its role; change_role preserves identity and ID.
# 5.4: Employee has (composition) a role-history collection. Immutable role snapshots
# and dated changes retain earlier pay rules. pay_on selects the effective role;
# monthly_pay means the rate effective today, not prorated pay across a month's roles.
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
import pytest


class Role(ABC):
    @abstractmethod
    def monthly_pay(self) -> int: ...


@dataclass(frozen=True)
class LecturerRole(Role):
    hours: int
    def monthly_pay(self):
        return self.hours * 120_000


@dataclass(frozen=True)
class HeadRole(Role):
    salary: int
    def monthly_pay(self):
        return self.salary + 3_000_000


class Employee:
    def __init__(self, emp_id, name, role, start_date):
        self.emp_id, self.name = emp_id, name
        self._role_history = [(role, start_date)]
    @property
    def role_history(self):
        return tuple(self._role_history)
    def change_role(self, new_role, start_date=None):
        start_date = start_date or date.today()
        if start_date <= self._role_history[-1][1]:
            raise ValueError('Role changes must have increasing start dates')
        self._role_history.append((new_role, start_date))
    def pay_on(self, day):
        for role, start in reversed(self._role_history):
            if start <= day:
                return role.monthly_pay()
        raise ValueError('Date precedes employment')
    def monthly_pay(self):
        return self.pay_on(date.today())


def test_promotion_and_history():
    employee = Employee(7, 'Ali', LecturerRole(100), date(2020, 1, 1))
    payroll_reference = employee
    employee.change_role(HeadRole(14000000), date(2020, 2, 1))
    assert employee is payroll_reference and employee.emp_id == 7
    assert employee.pay_on(date(2020, 1, 31)) == 12000000
    assert employee.pay_on(date(2020, 2, 1)) == 17000000
    assert employee.monthly_pay() == 17000000
    with pytest.raises(ValueError):
        employee.pay_on(date(2019, 1, 1))
    with pytest.raises(ValueError):
        employee.change_role(LecturerRole(50), date(2020, 1, 15))
