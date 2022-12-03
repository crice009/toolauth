from  import db


class base(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mac_addr = db.Column(db.String(64), index=True, unique=True)
    ip_addr = db.Column(db.String(120), index=True, unique=True)
    encrypt_pass = db.Column(db.String(128))
    ota_pass = db.Column(db.String(128))
    name = db.Column(db.String(128))
    reader_id = db.Column(db.Integer)
    tool_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)

    def __repr__(self):
        return "<base {}>".format(self.name)


class reader(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return "<reader {}>".format(self.id)


class tool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drupal_name = db.Column(db.String(128), index=True, unique=True)

    def __repr__(self):
        return "<tool {}>".format(self.id)


class reader_to_tool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reader_id = db.Column(db.Integer)
    tool_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)

    def __repr__(self):
        return "<reader_to_tool {}>".format(self.id)


class tool_to_vacuum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vacuum_id = db.Column(db.Integer)
    tool_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)

    def __repr__(self):
        return "<tool_to_vacuum {}>".format(self.id)
