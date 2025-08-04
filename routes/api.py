import datetime
import time

from flask import Blueprint, jsonify
from sqlalchemy import func

from api_auth import login_required, permission_required
from logger import logger
from models import Hardware, db, Software, Vulnerability

api_bp= Blueprint('api', __name__)



#add dummy data of 10 servers (hardware) and 2 software on each
#for each hardware we will have one vulnerabilty

@api_bp.post('/dummy-data') # post allows to receive  from the front end
@login_required
@permission_required('POST_DUMMY_DATA')
def dummy_data():
    epoch_time = int(time.time())
    hardwares = [
        Hardware(
            id=epoch_time + i,
            name = f"Server {epoch_time} {i}",
            type = f"Server",
            manufacturer = f"manufacturer",
            model = f"Server-{i}",
            location = f"UK",
            status = "Valid"
          )
        for i in range(1, 11)
    ]
    db.session.add_all(hardwares)
    #Random softwares
    softwares = [
       Software(
           name = f"App {i}",
           version =f'1.{i}.25',
           vendor = f"Vendor {i}",
           hardware_id =hardwares[i-1].id,
           status =f"Valid",
           installation_date = datetime.date(year=2024, month=i, day=1*3),
           licence_expiry_date = datetime.date(year=2025+i, month=i, day=1*3)
        )
        for i in range(1, 11)
    ]
    db.session.add_all(softwares)
    vulnerabilities = (
        db.session.query(Vulnerability)
        .filter((Vulnerability.version !='*') & (Vulnerability.version !='-')) # getting everything except * and -
        .order_by(func.random()) # Random function to get the data
        .all()
    )
    vulnerable_softwares = [
        Software(
            name=vulnerabilities[i-1].product,
            version=vulnerabilities[i-1].version,
            vendor=vulnerabilities[i-1].vendor,
            hardware_id=hardwares[i-1].id,
            status='Valid',
            installation_date=datetime.date(year=2024, month=i, day=1 * 3),
            licence_expiry_date=datetime.date(year=2025 + i, month=i, day=1 * 3)
        )

        for i in range(1, 11)
    ]

    for i in range(len (vulnerable_softwares)):
        logger.info(vulnerable_softwares[i])



    db.session.add_all(vulnerable_softwares)
    db.session.commit()

    return jsonify({'message' : 'Dummy data added'})




