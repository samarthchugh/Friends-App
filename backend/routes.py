from app import app, db
from flask import request, jsonify
from models import Friend


# Get all the friends
@app.route("/api/friends",methods=["GET"])
def get_friends():
    try:
        friends = Friend.query.all()  # Fetch all friends from the database
        return jsonify([friend.to_json() for friend in friends]), 200
    except Exception as e:
        print(f"Error: {str(e)}")  # Print the error for debugging
        return jsonify({"error": str(e)}), 500

# Create a friend 
@app.route("/api/friends",methods=["POST"])
def create_friend():
    try:
        data = request.json
        
        required_fields = ["name","role","description","gender"]
        for field in required_fields:
            if field not in data or not data.get(field):
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        name=data.get("name")
        role=data.get("role")
        description=data.get("description")
        gender=data.get("gender")
        
        # Fetch avatar image based on the gender
        if gender=='male':
            img_url= f"https://avatar.iran.liara.run/public/boy?username={name}"
        elif gender=='female':
            img_url = f"https://avatar.iran.liara.run/public/girl?username={name}"
        else:
            img_url = None
            
        new_friend = Friend(name=name, role=role, description=description, gender=gender, image_url=img_url)
        
        db.session.add(new_friend)
        
        db.session.commit()
        
        return jsonify(new_friend.to_json()),201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":str(e)}),500
    
    
# Delete the Friend
@app.route("/api/friends/<int:id>",methods=['DELETE'])
def delete_friend(id):
    try:
        friend = Friend.query.get(id)
        if friend is None:
            return jsonify({"error":"Friend not found"}),404
        
        db.session.delete(friend)
        db.session.commit()
        return jsonify({"msg":"friend deleted"}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":str(e)}),500
    
    
# Update a friend profile
@app.route("/api/friends/<int:id>",methods=['PATCH'])
def update_friend(id):
    try:
        friend = Friend.query.get(id)
        if friend is None:
            return jsonify({"error":"Friend not Found"}),404
        
        data = request.json
        
        friend.name=data.get("name",friend.name)
        friend.role=data.get("role",friend.role)
        friend.description=data.get("description",friend.description)
        friend.gender=data.get("gender",friend.gender)

        db.session.commit()
        return jsonify(friend.to_json()),200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":str(e)}),500