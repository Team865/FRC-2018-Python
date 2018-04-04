package ca.warp7.robot.auto;

import static ca.warp7.robot.Constants.CUBE_DISTANCE_M;

import com.stormbots.MiniPID;

import static ca.warp7.robot.Constants.CUBE_DISTANCE_B;

import ca.warp7.robot.Robot;
import ca.warp7.robot.misc.DataPool;
import ca.warp7.robot.misc.RTS;
import ca.warp7.robot.subsystems.Drive;
import ca.warp7.robot.subsystems.Intake;
import ca.warp7.robot.subsystems.Lift;
import ca.warp7.robot.subsystems.Limelight;
import ca.warp7.robot.subsystems.Navx;
import edu.wpi.first.wpilibj.Timer;
import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;

public class AutonomousBase {
	public static DataPool autoPool = new DataPool("auto");
	private Drive drive = Robot.drive;
	private Navx navx = Robot.navx;
	private Limelight limelight = Robot.limelight;
	private Intake intake = Robot.intake;
	private Lift lift = Robot.lift;

	private MiniPID turnPID;
	private MiniPID turnSoftPID;
	private MiniPID distancePID;

	public AutoFunctions autoFunc = new AutoFunctions();
	private CustomFunctions customFunc = new CustomFunctions();

	private int step = 0;

	public void autonomousPeriodic(String gameData, int pin) {
		if (pin == 0) { // None
			System.out.println("pin 0 active :None:");
			if (gameData.equals("RRR"))
				None_RRR();
			else if (gameData.equals("LLL"))
				None_LLL();
			else if (gameData.equals("LRL"))
				None_LRL();
			else if (gameData.equals("RLR"))
				None_RLR();
		} else if (pin == 1) { // Left
			System.out.println("pin 1 active :Left:");
			if (gameData.equals("RRR"))
				Left_RRR();
			else if (gameData.equals("LLL"))
				Left_LLL();
			else if (gameData.equals("LRL"))
				Left_LRL();
			else if (gameData.equals("RLR"))
				Left_RLR();
		} else if (pin == 2) { // Middle
			System.out.println("pin 2 active :Middle:");
			if (gameData.equals("RRR"))
				Middle_RRR();
			else if (gameData.equals("LLL"))
				Middle_LLL();
			else if (gameData.equals("LRL"))
				Middle_LRL();
			else if (gameData.equals("RLR"))
				Middle_RLR();
		} else if (pin == 3) { // Right
			System.out.println("pin 3 active :Right:");
			if (gameData.equals("RRR"))
				Right_RRR();
			else if (gameData.equals("LLL"))
				Right_LLL();
			else if (gameData.equals("LRL"))
				Right_LRL();
			else if (gameData.equals("RLR"))
				Right_RLR();
		}
	}

	private void Left_RLR() {
		switch (step) {
		case (0):
			if (autoFunc.driveDistance(585)) {
				lift.setLoc(1);
				step++;
			}
			break;
		case (1):
			if (autoFunc.angleRelTurn(22.5)) {
				autoFunc.setSpeedLimit(0.75);
				step++;
			}
			break;
		case (2):
			if (autoFunc.driveDistance(100)) {
				System.out.println("Exiting drive because im done");
				autoFunc.setSpeedLimit(1);
				intake.setSpeed(-1);
				Timer.delay(0.2);
				intake.setSpeed(0);
				step++;
			}
			break;
	
		case (3):
			if (autoFunc.angleRelTurn(90)) {
				step++;
			}
			break;
		}
	}

	private void Left_RRR() {
		switch (step) {
		case (0): {
			intake.setSpeed(0.2);
			step++;
			break;
		}
		case (1):
			if (autoFunc.driveDistance(535)) {
				System.out.println("Exiting drive because im done");
				step++;
			}
			break;
		case (2):
			if (autoFunc.angleRelTurn(90)) {
				step++;
			}
			break;
		case (3):
			if (autoFunc.driveDistance(485)) {
				System.out.println("Exiting drive because im done");
				lift.setLoc(1);
				step++;
			}
			break;
		
		case (4):
			if (autoFunc.angleRelTurn(-90)) {
				autoFunc.setSpeedLimit(0.5);
				step++;
			}
			break;
			
		case (5):
			if (autoFunc.driveDistance(95)) {
				System.out.println("Exiting drive because im done");
				intake.setSpeed(-1);
				Timer.delay(0.2);
				intake.setSpeed(0);
				step++;
			}
			break;
			
		}
	}

	private void Left_LLL() { //OUTDATED
		switch (step) {
		case (0):
			if (autoFunc.driveDistance(585)) {
				System.out.println("Exiting drive because im done");
				lift.setLoc(1);
				step++;
			}
			break;
		case (1):
			if (autoFunc.angleRelTurn(22.5)) {
				autoFunc.setSpeedLimit(0.75);
				step++;
			}
			break;
		case (2):
			if (autoFunc.driveDistance(100)) {
				System.out.println("Exiting drive because im done");
				autoFunc.setSpeedLimit(1);
				intake.setSpeed(-1);
				Timer.delay(0.2);
				intake.setSpeed(0);
				step++;
			}
			break;
	
		case (3):
			if (autoFunc.angleRelTurn(90)) {
				step++;
			}
			break;
		}
	}

	private void Left_LRL() {
		
	}

	private void Right_RLR() {

	}

	private void Right_LRL() {
		// TODO Auto-generated method stub

	}

	private void Right_LLL() {
		// TODO Auto-generated method stub

	}

	private void Right_RRR() {

	}

	// Middle switch left
	private void Middle_LLL() {
		switch (step) {
		case (0):
			if (autoFunc.angleRelTurn(-22.5)) {
				lift.setLoc(0.4);
				
				step++;
			}
			break;

		case (1): {
			if (autoFunc.driveDistance(280)) {
				intake.setSpeed(-1);
				Timer.delay(0.2);
				intake.setSpeed(0);
				step++;
			}
		}
	}
	}

	// Middle switch right
	private void Middle_RRR() {

	}

	// Middle switch right
	private void Middle_RLR() {

	}

	// Middle switch left
	private void Middle_LRL() {
		switch (step) {
		case (0):
			if (autoFunc.angleRelTurn(-22.5)) {
				lift.setLoc(0.4);
				step++;
			}
			break;

		case (1): {
			if (autoFunc.driveDistance(280)) {
				intake.setSpeed(-1);
				Timer.delay(0.2);
				intake.setSpeed(0);
				step++;
			}
		}
	}
	}

	private void None_RLR() { //TESTING
		autoFunc.setSpeedLimit(0.8);
		switch (step) {
		case (0):
			if (autoFunc.driveDistance(300)) 
				step++;
			break;
		/*case (1): 
			if (autoFunc.angleRelTurn(90)) 
				step++;
			break;
		case (2): 
			if (autoFunc.angleRelTurn(90)) 
				step++;
			break;
		case (3): 
			if (autoFunc.angleRelTurn(180)) 
				step++;
			break;
		case (4): 
				if (autoFunc.angleRelTurn(180)) 
					step++;
				break;
		*/
	}
	}
	

	private void None_LRL() {
		// TODO Auto-generated method stub
	switch(step) {
	case (0):
		if (autoFunc.angleRelTurn(145, () -> customFunc.turnDrop(20,50))) {
			autoFunc.setSpeedLimit(0.75);
			intake.setSpeed(1);
			step++;
		}
		break;
	}
	}

	private void None_LLL() {
		// TODO Auto-generated method stub
		switch (step) {
		case (0): {
			intake.setSpeed(0.3);
			step++;
			break;
		}
		case (1):
			if (autoFunc.driveDistance(585+40)) {
				lift.setLoc(1);
				Timer.delay(2);
				step++;
			}
			break;
		
		case (2):
			if (autoFunc.angleRelTurn(143, () -> customFunc.turnDrop(20,50))) {
				autoFunc.setSpeedLimit(0.75);
				intake.setSpeed(1);
				step++;
			}
			break;
		case (3):
			if(autoFunc.alignIntakeCube(170,4)) {
				step++;
			}
			break;
		
		case (4):
			if (autoFunc.driveDistance(-10)) {
				intake.setSpeed(0.3);
				lift.setLoc(0.5);
				Timer.delay(1);
				step++;
			}
			break;
			
		case (5):
			if (autoFunc.driveDistance(25)) {
				intake.setSpeed(-1);
				Timer.delay(0.2);
				intake.setSpeed(0);
				step++;
			}
			break;
		}
	}

	private void None_RRR() {
		// TODO Auto-generated method stub
		switch (step) {
		case (0): 
			autoFunc.setSpeedLimit(0.3);
			intake.setSpeed(1);
			step++;
			break;
		case (1):
			if(autoFunc.alignIntakeCube(300,10)) {
				step++;
			}
			break;
		}
	}
}