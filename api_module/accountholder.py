from account import BankAccountCommand, BankAccount

class AccountCommand:
    def __init__(self, session_holder):
        self.session_holder = session_holder

    def withdraw(self, uuid, amount):
        balance = self.session_holder.get_balance_by_uuid(uuid)
        if balance is None:
            return False
        account_info = BankAccount(balance)
        c_exec = BankAccountCommand(account_info, action=BankAccountCommand.Action.WITHDRAW, amount=amount)
        c_exec.invoke()
        return account_info.balance if c_exec.success else False

    def deposit(self, uuid, amount):
        balance = self.session_holder.get_balance_by_uuid(uuid)
        if balance is None:
            return False
        account_info = BankAccount(balance)
        c_exec = BankAccountCommand(account_info, action=BankAccountCommand.Action.DEPOSIT, amount=amount)  # Use enum
        c_exec.invoke()
        return account_info.balance

    def take_action(self, uuid, action, amount):
        if action == 'WITHDRAW':
            return self.withdraw(uuid, amount)
        elif action == 'DEPOSIT':
            return self.deposit(uuid, amount)
        return False