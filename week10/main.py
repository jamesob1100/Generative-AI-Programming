"""Bus ticketing system with menu-driven interface."""

import hashlib
import sqlite3
from datetime import date, timedelta

from create_database import DB_PATH


MESSAGES = {
    "welcome": "=== Transport Booking System ===",
    "home_menu": "\nHome Menu:\n1. Log in\n2. Create an account\n3. Exit\nEnter choice: ",
    "username_prompt": "Username: ",
    "password_prompt": "Password: ",
    "login_failed": "Invalid username or password.",
    "login_success": "Welcome back, {}!",
    "account_exists": "Account already exists.",
    "account_created": "Account created for '{}'.",
    "admin_menu": (
        "\nAdmin Menu:\n1. View existing services\n2. Create a service\n3. Log out\n"
        "Enter choice: "
    ),
    "customer_menu": (
        "\nCustomer Menu:\n1. View future bus runs\n2. Buy tickets\n3. View my tickets\n"
        "4. Log out\nEnter choice: "
    ),
    "services_header": "\nAvailable Services:",
    "no_services": "No services available.",
    "service_name": "Service name: ",
    "service_created": "Service '{}' created.",
    "logged_out": "Logged out.",
    "runs_header": "\nAvailable Bus Runs:",
    "no_runs": "No runs available.",
    "run_format": "{}. {} - {}",
    "select_run": "Select run number: ",
    "invalid_run": "Invalid run selection.",
    "tickets_prompt": "Number of tickets: ",
    "insufficient_seats": "Not enough seats available.",
    "confirm_booking": "Press Enter to confirm or type 'esc' to cancel: ",
    "booking_confirmed": "Booking confirmed!",
    "booking_cancelled": "Booking cancelled.",
    "my_tickets_header": "\nYour Tickets:",
    "no_tickets": "You have no tickets.",
    "ticket_format": "{} tickets for {} on {}",
    "invalid_choice": "Invalid choice.",
    "invalid_input": "Invalid input.",
}


class User:
    """Represents a user in the system."""

    def __init__(self, user_id: int, username: str, admin: bool):
        """
        Initialize a user.

        Parameters:
            user_id: Unique user identifier
            username: User's login name
            admin: Whether user is admin

        Returns:
            None

        Tests:
            - check that user is created with correct attributes
            - check that admin flag is properly set
        """
        self.user_id = user_id
        self.username = username
        self.admin = admin


class BusModel:
    """Represents a bus model with seating capacity."""

    def __init__(self, model_id: int, name: str, seats: int):
        """
        Initialize a bus model.

        Parameters:
            model_id: Unique model identifier
            name: Model name
            seats: Number of seats

        Returns:
            None

        Tests:
            - check that bus model is created with correct attributes
            - check that seat count is stored properly
        """
        self.model_id = model_id
        self.name = name
        self.seats = seats


class PhysicalBus:
    """Represents a physical bus assigned to a service."""

    def __init__(
        self, bus_id: int, service_id: int, model_id: int, schedule_type: str
    ):
        """
        Initialize a physical bus.

        Parameters:
            bus_id: Unique bus identifier
            service_id: Service this bus operates on
            model_id: Bus model identifier
            schedule_type: Schedule type (weekends/workdays)

        Returns:
            None

        Tests:
            - check that bus is created with correct attributes
            - check that bus-service relationship is stored
        """
        self.bus_id = bus_id
        self.service_id = service_id
        self.model_id = model_id
        self.schedule_type = schedule_type


class BusService:
    """Represents a bus service route."""

    def __init__(self, service_id: int, name: str):
        """
        Initialize a bus service.

        Parameters:
            service_id: Unique service identifier
            name: Service route name

        Returns:
            None

        Tests:
            - check that service is created with correct attributes
            - check that service name is stored properly
        """
        self.service_id = service_id
        self.name = name


class Run:
    """Represents a scheduled bus run."""

    def __init__(self, run_id: int, service_id: int, run_date: str):
        """
        Initialize a bus run.

        Parameters:
            run_id: Unique run identifier
            service_id: Service this run belongs to
            run_date: Run date in ISO format

        Returns:
            None

        Tests:
            - check that run is created with correct attributes
            - check that date is stored properly
        """
        self.run_id = run_id
        self.service_id = service_id
        self.run_date = run_date


class Ticket:
    """Represents a ticket purchase."""

    def __init__(self, ticket_id: int, user_id: int, run_id: int, number: int):
        """
        Initialize a ticket.

        Parameters:
            ticket_id: Unique ticket identifier
            user_id: User who bought the ticket
            run_id: Run the ticket is for
            number: Number of tickets

        Returns:
            None

        Tests:
            - check that ticket is created with correct attributes
            - check that ticket quantity is stored properly
        """
        self.ticket_id = ticket_id
        self.user_id = user_id
        self.run_id = run_id
        self.number = number


def hash_password(password: str) -> str:
    """
    Hash a password using SHA-256.

    Parameters:
        password: Plain text password

    Returns:
        Hexadecimal hash of the password

    Tests:
        - check that same password produces same hash
        - check that different passwords produce different hashes
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def get_connection() -> sqlite3.Connection:
    """
    Get database connection.

    Parameters:
        None

    Returns:
        SQLite database connection

    Tests:
        - check that connection is established successfully
        - check that foreign keys are enabled
    """
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def login_user(username: str, password: str) -> User | None:
    """
    Authenticate user and return user object.

    Parameters:
        username: User's login name
        password: User's password

    Returns:
        User object if authentication successful, None otherwise

    Tests:
        - check that valid credentials return user object
        - check that invalid credentials return None
        - check that password is properly hashed for comparison
    """
    conn = get_connection()
    cursor = conn.cursor()
    hashed = hash_password(password)
    row = cursor.execute(
        "SELECT id, username, admin FROM user WHERE username = ? AND password = ?",
        (username, hashed),
    ).fetchone()
    conn.close()
    return User(row[0], row[1], bool(row[2])) if row else None


def username_exists(username: str) -> bool:
    """
    Check if username already exists in database.

    Parameters:
        username: Username to check

    Returns:
        True if username exists, False otherwise

    Tests:
        - check that existing username is detected
        - check that non-existing username returns False
    """
    conn = get_connection()
    cursor = conn.cursor()
    row = cursor.execute(
        "SELECT id FROM user WHERE username = ?", (username,)
    ).fetchone()
    conn.close()
    return row is not None


def create_user(username: str, password: str) -> bool:
    """
    Create new user account.

    Parameters:
        username: New username
        password: New password

    Returns:
        True if account created, False if username exists

    Tests:
        - check that new account is created successfully
        - check that duplicate username is rejected
        - check that password is hashed
        - check that username validation occurs before database insert
    """
    if username_exists(username):
        return False

    conn = get_connection()
    cursor = conn.cursor()
    hashed = hash_password(password)
    cursor.execute(
        "INSERT INTO user (admin, username, password) VALUES (?, ?, ?)",
        (0, username, hashed),
    )
    conn.commit()
    conn.close()
    return True


def get_all_services() -> list[BusService]:
    """
    Get all bus services.

    Parameters:
        None

    Returns:
        List of BusService objects

    Tests:
        - check that all services are returned
        - check that empty list is returned when no services exist
        - check that services are ordered consistently
    """
    conn = get_connection()
    cursor = conn.cursor()
    rows = cursor.execute("SELECT id, name FROM service").fetchall()
    conn.close()
    return [BusService(row[0], row[1]) for row in rows]


def create_service(name: str) -> bool:
    """
    Create new bus service with buses and runs.

    Parameters:
        name: Service name

    Returns:
        True if service created successfully

    Tests:
        - check that service is created in database
        - check that 2 buses are created for the service
        - check that 7 runs are created for the service
        - check that runs are created for next 7 days
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO service (name) VALUES (?)", (name,))
    service_id = cursor.lastrowid

    bus_models = cursor.execute("SELECT id FROM bus_model").fetchall()
    model_ids = [m[0] for m in bus_models]

    cursor.execute(
        "INSERT INTO bus (service_id, bus_model_id, schedule_type, weekend, workday) "
        "VALUES (?, ?, ?, ?, ?)",
        (service_id, model_ids[0], "weekends", 1, 0),
    )
    cursor.execute(
        "INSERT INTO bus (service_id, bus_model_id, schedule_type, weekend, workday) "
        "VALUES (?, ?, ?, ?, ?)",
        (service_id, model_ids[1], "workdays", 0, 1),
    )

    today = date.today()
    for offset in range(7):
        run_date = (today + timedelta(days=offset)).isoformat()
        cursor.execute(
            "INSERT INTO run (service_id, run_date) VALUES (?, ?)",
            (service_id, run_date),
        )

    conn.commit()
    conn.close()
    return True


def get_future_runs() -> list[tuple[int, BusService, Run]]:
    """
    Get all future bus runs with service information.

    Parameters:
        None

    Returns:
        List of tuples (index, BusService, Run)

    Tests:
        - check that only future runs are returned
        - check that runs are ordered by service name then date
        - check that service information is included
    """
    conn = get_connection()
    cursor = conn.cursor()
    today = date.today().isoformat()
    rows = cursor.execute(
        """
        SELECT r.id, s.id, s.name, r.run_date
        FROM run r
        JOIN service s ON r.service_id = s.id
        WHERE r.run_date >= ?
        ORDER BY s.name, r.run_date
        """,
        (today,),
    ).fetchall()
    conn.close()

    runs = []
    for idx, (run_id, service_id, service_name, run_date) in enumerate(rows, 1):
        service = BusService(service_id, service_name)
        run = Run(run_id, service_id, run_date)
        runs.append((idx, service, run))
    return runs


def get_available_seats(run_id: int) -> int:
    """
    Get number of available seats for a run.

    Parameters:
        run_id: Run identifier

    Returns:
        Number of available seats

    Tests:
        - check that total seats are calculated correctly
        - check that booked tickets are subtracted
        - check that multiple ticket entries are summed
    """
    conn = get_connection()
    cursor = conn.cursor()

    total_seats = cursor.execute(
        """
        SELECT SUM(bm.seats)
        FROM run r
        JOIN service s ON r.service_id = s.id
        JOIN bus b ON b.service_id = s.id
        JOIN bus_model bm ON b.bus_model_id = bm.id
        WHERE r.id = ?
        """,
        (run_id,),
    ).fetchone()[0]

    booked = cursor.execute(
        "SELECT COALESCE(SUM(number), 0) FROM ticket WHERE run_id = ?", (run_id,)
    ).fetchone()[0]

    conn.close()
    return (total_seats or 0) - booked


def buy_tickets(user_id: int, run_id: int, number: int) -> bool:
    """
    Purchase tickets for a run.

    Parameters:
        user_id: User buying tickets
        run_id: Run to buy tickets for
        number: Number of tickets to buy

    Returns:
        True if purchase successful

    Tests:
        - check that tickets are created in database
        - check that insufficient seats is detected
        - check that existing ticket entries are updated or new ones created
    """
    conn = get_connection()
    cursor = conn.cursor()

    existing = cursor.execute(
        "SELECT id, number FROM ticket WHERE user_id = ? AND run_id = ?",
        (user_id, run_id),
    ).fetchone()

    if existing:
        new_total = existing[1] + number
        cursor.execute("UPDATE ticket SET number = ? WHERE id = ?", (new_total, existing[0]))
    else:
        cursor.execute(
            "INSERT INTO ticket (user_id, run_id, number) VALUES (?, ?, ?)",
            (user_id, run_id, number),
        )

    conn.commit()
    conn.close()
    return True


def get_user_tickets(user_id: int) -> list[Ticket]:
    """
    Get all tickets for a user.

    Parameters:
        user_id: User identifier

    Returns:
        List of Ticket objects

    Tests:
        - check that all user tickets are returned
        - check that empty list is returned when user has no tickets
        - check that ticket quantities are correct
    """
    conn = get_connection()
    cursor = conn.cursor()
    rows = cursor.execute(
        "SELECT id, user_id, run_id, number FROM ticket WHERE user_id = ?",
        (user_id,),
    ).fetchall()
    conn.close()
    return [Ticket(row[0], row[1], row[2], row[3]) for row in rows]


def get_ticket_details(ticket: Ticket) -> tuple[str, str]:
    """
    Get service name and date for a ticket.

    Parameters:
        ticket: Ticket object

    Returns:
        Tuple of (service_name, run_date)

    Tests:
        - check that correct service is retrieved
        - check that correct date is retrieved
    """
    conn = get_connection()
    cursor = conn.cursor()
    row = cursor.execute(
        """
        SELECT s.name, r.run_date
        FROM ticket t
        JOIN run r ON t.run_id = r.id
        JOIN service s ON r.service_id = s.id
        WHERE t.id = ?
        """,
        (ticket.ticket_id,),
    ).fetchone()
    conn.close()
    return (row[0], row[1]) if row else ("", "")


def display_services(services: list[BusService]) -> None:
    """
    Display list of services.

    Parameters:
        services: List of BusService objects

    Returns:
        None

    Tests:
        - check that services are displayed in order
        - check that no services message is shown when list is empty
    """
    if not services:
        print(MESSAGES["no_services"])
        return
    for service in services:
        print(f"{service.service_id}. {service.name}")


def display_runs(runs: list[tuple[int, BusService, Run]]) -> None:
    """
    Display list of runs.

    Parameters:
        runs: List of run tuples (index, service, run)

    Returns:
        None

    Tests:
        - check that runs are displayed with index, service, and date
        - check that no runs message is shown when list is empty
    """
    if not runs:
        print(MESSAGES["no_runs"])
        return
    for idx, service, run in runs:
        print(MESSAGES["run_format"].format(idx, service.name, run.run_date))


def display_user_tickets(user_id: int) -> None:
    """
    Display user's tickets.

    Parameters:
        user_id: User identifier

    Returns:
        None

    Tests:
        - check that all tickets are displayed
        - check that no tickets message is shown when user has no tickets
    """
    print(MESSAGES["my_tickets_header"])
    tickets = get_user_tickets(user_id)
    if not tickets:
        print(MESSAGES["no_tickets"])
        return
    for ticket in tickets:
        service_name, run_date = get_ticket_details(ticket)
        print(MESSAGES["ticket_format"].format(ticket.number, service_name, run_date))


def admin_menu(user: User) -> None:
    """
    Handle admin user menu.

    Parameters:
        user: Current admin user

    Returns:
        None

    Tests:
        - check that all admin menu options are functional
        - check that invalid choices are handled
        - check that logout is possible
    """
    while True:
        choice = input(MESSAGES["admin_menu"])
        if choice == "1":
            print(MESSAGES["services_header"])
            display_services(get_all_services())
        elif choice == "2":
            name = input(MESSAGES["service_name"])
            create_service(name)
            print(MESSAGES["service_created"].format(name))
        elif choice == "3":
            print(MESSAGES["logged_out"])
            break
        else:
            print(MESSAGES["invalid_choice"])


def customer_menu(user: User) -> None:
    """
    Handle customer user menu.

    Parameters:
        user: Current customer user

    Returns:
        None

    Tests:
        - check that all customer menu options are functional
        - check that ticket buying process works
        - check that cancellation is handled
        - check that invalid choices are handled
    """
    while True:
        choice = input(MESSAGES["customer_menu"])
        if choice == "1":
            print(MESSAGES["runs_header"])
            display_runs(get_future_runs())
        elif choice == "2":
            runs = get_future_runs()
            if not runs:
                print(MESSAGES["no_runs"])
                continue
            display_runs(runs)
            try:
                selection = int(input(MESSAGES["select_run"]))
                if selection < 1 or selection > len(runs):
                    print(MESSAGES["invalid_run"])
                    continue
                _, _, selected_run = runs[selection - 1]
                num_tickets = int(input(MESSAGES["tickets_prompt"]))
                available = get_available_seats(selected_run.run_id)
                if num_tickets > available:
                    print(MESSAGES["insufficient_seats"])
                    continue
                confirm = input(MESSAGES["confirm_booking"])
                if confirm.lower() == "esc":
                    print(MESSAGES["booking_cancelled"])
                else:
                    buy_tickets(user.user_id, selected_run.run_id, num_tickets)
                    print(MESSAGES["booking_confirmed"])
            except ValueError:
                print(MESSAGES["invalid_input"])
        elif choice == "3":
            display_user_tickets(user.user_id)
        elif choice == "4":
            print(MESSAGES["logged_out"])
            break
        else:
            print(MESSAGES["invalid_choice"])


def home_menu() -> None:
    """
    Handle main menu and user session.

    Parameters:
        None

    Returns:
        None

    Tests:
        - check that login works for existing users
        - check that account creation works
        - check that invalid login is rejected
        - check that proper menu is shown for admin vs customer
    """
    print(MESSAGES["welcome"])
    while True:
        choice = input(MESSAGES["home_menu"])
        if choice == "1":
            username = input(MESSAGES["username_prompt"])
            password = input(MESSAGES["password_prompt"])
            user = login_user(username, password)
            if user:
                print(MESSAGES["login_success"].format(username))
                if user.admin:
                    admin_menu(user)
                else:
                    customer_menu(user)
            else:
                print(MESSAGES["login_failed"])
        elif choice == "2":
            username = input(MESSAGES["username_prompt"])
            password = input(MESSAGES["password_prompt"])
            if create_user(username, password):
                print(MESSAGES["account_created"].format(username))
            else:
                print(MESSAGES["account_exists"])
        elif choice == "3":
            break
        else:
            print(MESSAGES["invalid_choice"])


def main() -> None:
    """
    Main entry point for the bus ticketing system.

    Parameters:
        None

    Returns:
        None

    Tests:
        - check that application starts successfully
        - check that home menu is displayed
        - check that application exits cleanly
    """
    home_menu()


if __name__ == "__main__":
    main()
