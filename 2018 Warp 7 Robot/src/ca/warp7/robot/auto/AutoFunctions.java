package ca.warp7.robot.auto;

import static ca.warp7.robot.Constants.CUBE_DISTANCE_B;
import static ca.warp7.robot.Constants.CUBE_DISTANCE_M;

import com.stormbots.MiniPID;

import ca.warp7.robot.Robot;
import ca.warp7.robot.subsystems.Drive;
import ca.warp7.robot.subsystems.Intake;
import ca.warp7.robot.subsystems.Lift;
import ca.warp7.robot.subsystems.Limelight;
import ca.warp7.robot.subsystems.Navx;
import edu.wpi.first.wpilibj.Timer;

public class AutoFunctions {
	private MiniPID turnPID;
	private MiniPID distancePID;
	private int ticks;

	private Drive drive = Robot.drive;
	private Navx navx = Robot.navx;
	private Limelight limelight = Robot.limelight;
	private boolean angleReset;
	private boolean distanceReset;
	private int totalTicks=0;//for testing, delete this
	private static final double speed = 1;
	private double speedLimit = 1;
	
	public double wantedAngle = 0;

	public AutoFunctions() { //march 16 working = 0.0155, 0.0029, 0.23
		turnPID = new MiniPID(0.009,0.01, 0.21); 
		turnPID.setOutputLimits(1);
		turnPID.setOutputRampRate(0.083);
		turnPID.setMaxIOutput(0.175);
		
		distancePID = new MiniPID(0.02, 0.0013, 0.22);
		distancePID.setOutputLimits(1);
		distancePID.setMaxIOutput(0.01);
		
		angleReset=true;
		distanceReset=true;
	}

	public boolean driveDistance(double dist) {
		if (distanceReset) {
			navx.resetAngle();
			drive.resetDistance();
			distancePID.setSetpoint(dist);
			ticks = 0;
			turnPID.setSetpoint(0);
			distanceReset=false;
			System.out.println("drive reset complete");
			//turn pid i term fix
			return false;
		}
		double turnSpeed = turnPID.getOutput(navx.getAngle() % 360, 0);
		double curDistance = getOverallDistance();
		double driveSpeed = distancePID.getOutput(curDistance,dist);
		System.out.println(
				"driving. curDist= " + curDistance + "setPoint= " +dist+ " deltaAng= " + (0 - (navx.getAngle() % 360)));
		if (within(curDistance, dist, 15))
			ticks++;
		else
			ticks=0;
		if ((within(curDistance, dist, 15)) && ticks > 20) {
			autoDrive(0, 0);
			distanceReset=true;
			System.out.println("driving complete");
			return true;
		} else {
			if (turnSpeed < 0) {// turn left
				turnSpeed = -(turnSpeed);
		
				autoDrive(driveSpeed-turnSpeed,driveSpeed);
			} else { // turn right
				autoDrive(driveSpeed,driveSpeed-turnSpeed);
			}
		}
		return false;
	}
	
	public boolean driveDistance(double dist, Runnable func) {
		if (distanceReset) {
			navx.resetAngle();
			drive.resetDistance();
			distancePID.setSetpoint(dist);
			ticks = 0;
			turnPID.setSetpoint(0);
			distanceReset=false;
			wantedAngle=0;
			System.out.println("drive reset complete");
			//turn pid i term fix
			return false;
		}
		func.run();
		double turnSpeed = turnPID.getOutput(navx.getAngle() % 360, wantedAngle);
		double curDistance = getOverallDistance();
		double driveSpeed = distancePID.getOutput(curDistance,dist);
		System.out.println(
				"driving. curDist= " + curDistance + "setPoint= " +dist+ " deltaAng= " + (0 - (navx.getAngle() % 360)));
		if (within(curDistance, dist, 15))
			ticks++;
		else
			ticks=0;
		if ((within(curDistance, dist, 15)) && ticks > 20) {
			autoDrive(0, 0);
			distanceReset=true;
			System.out.println("driving complete");
			return true;
		} else {
			if (turnSpeed < 0) {// turn left
				turnSpeed = -(turnSpeed);
		
				autoDrive(driveSpeed-turnSpeed,driveSpeed);
			} else { // turn right
				autoDrive(driveSpeed,driveSpeed-turnSpeed);
			}
		}
		return false;
	}
		
	public boolean angleRelTurn(double setP) {
		if (angleReset) {
			totalTicks=0;//test, delete this
			navx.resetAngle();
			Timer.delay(0.05);
			ticks=0;
			turnPID.setSetpoint(setP);
			angleReset=false;
			System.out.println("turn reset complete");
			return false;
		} else {
			totalTicks++;//test, delete this
			double curAngle = navx.getAngle() % 360;
			double turnSpeed = turnPID.getOutput(curAngle);
			if (within(curAngle, setP, 2)) {
				ticks++;
				turnSpeed = 0;
			} else
				ticks = 0;
			System.out.println("ticks " + ticks);
			if (ticks > 5) {
				angleReset=true;
				System.out.println("turn complete after ticks=" + totalTicks); //test, delete this
				autoDrive(0, 0);
				return true;
			} else {
				System.out.println("turning. cAn= " + curAngle + " setP= " + setP + " TS=" + turnSpeed+"totTicks= "+totalTicks);

				autoDrive(turnSpeed, -turnSpeed);

			}
		}
		return false;

	}

	public boolean angleRelTurn(double setP, Runnable func) {
		if (angleReset) {
			navx.resetAngle();
			turnPID.setSetpoint(setP);
			turnPID.setMaxIOutput(0.32);
			angleReset=false;
			System.out.println("turn reset complete");
			return false;
		}
		else {
			func.run();
			double curAngle = navx.getAngle() % 360;
			double turnSpeed=turnPID.getOutput(curAngle);
			if (within(curAngle, setP, 1)) {
				ticks++;
				turnSpeed = 0;
			} else
				ticks = 0;
			System.out.println("ticks " + ticks);
			if (ticks > 7) {
				angleReset=true;
				System.out.println("turnDrop complete");
				return true;
			} else {
				System.out.println("turning. cAn= " + curAngle + " setP= " + setP + " TS=" + turnSpeed);
				autoDrive(turnSpeed, -turnSpeed);

			}
		}
		return false;

	}

	public boolean alignIntakeCube(double dist, double angleThresh) {	
		if (distanceReset) {
			navx.resetAngle();
			drive.resetDistance();
			distancePID.setSetpoint(dist);
			ticks = 0;
			distanceReset=false;
			System.out.println("align intake drive reset complete");
			return false;
		}
		double cubeAngleOffset = limelight.getXOffset();
		double turnSpeed = 1-Math.abs(cubeAngleOffset/angleThresh);
		if (turnSpeed < 0)
			turnSpeed = 0;
		double curDistance = getOverallDistance();
		double driveSpeed = distancePID.getOutput(curDistance);
		System.out.println(cubeAngleOffset + ":" + turnSpeed);
		if (within(curDistance, dist, 15))
			ticks++;
		else
			ticks=0;
		if ((within(curDistance, dist, 15)) && ticks > 20) {
			autoDrive(0, 0);
			distanceReset=true;
			return true;
		} else {
			if (cubeAngleOffset >= 0)//turn right
				autoDrive(driveSpeed,driveSpeed*turnSpeed);
			else { //turn left
				autoDrive(driveSpeed*turnSpeed,driveSpeed);
			}
		}
		return false;
	}
	
	private void autoDrive(double left, double right) {
		if (left > speedLimit)
			left = speedLimit;
		else if (left < -speedLimit)
			left = -speedLimit;
		
		if (right > speedLimit)
			right = speedLimit;
		else if (right < -speedLimit)
			right = -speedLimit;
		
		drive.tankDrive(speed*left,speed*right);
	}
	
	public void setSpeedLimit(double speedLimit) {
		this.speedLimit = Math.abs(speedLimit);
	}
	
	private boolean within(double angle, double setAngle, double thresh) {
		return (setAngle - thresh) < angle && (setAngle + thresh) > angle;
	}

	private double getOverallDistance() {
		return (-drive.getLeftDistance() + -drive.getRightDistance()) / 2;
	}
}