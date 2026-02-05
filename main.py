from principal import app, database
from principal.models import User
import click

@app.cli.command('set-admin')
@click.argument('email')
def set_admin(email):
    """Sets a user as an admin."""
    user = User.query.filter_by(email=email).first()
    if user:
        user.is_admin = True
        database.session.commit()
        print(f"{user.name} is now an admin.")
    else:
        print("User not found.")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
