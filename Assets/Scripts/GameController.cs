using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class GameController : MonoBehaviour {
	[SerializeField]
	private Sprite[] colorSprites = new Sprite[6];
	[SerializeField]
	private GameObject[] secretCodeObjects = new GameObject[4];
	[SerializeField]
	private GameObject gameCircle;
	[SerializeField]
	private Canvas canvas;
	[SerializeField]
	private GameObject stateCircle;
	[SerializeField]
	private Sprite whiteCircle;
	[SerializeField]
	private GameObject hintArray;
	[SerializeField]
	private GameObject hintCircle;
	[SerializeField]
	private GameObject gameText;
	[SerializeField]
	private Sprite redCircle;
	private GameObject[] gameCircleArray;
	private int numColorsFilled = 0;
	private int numRows = 0;
	private float startPos_X = -117f;
	private float startPos_Y = 120f;
	private bool gameOver = false;
	private int rowLength;

	void Start(){
		rowLength = secretCodeObjects.Length;
		BuildSecretCode ();
		BuildGameCircleRow ();
	}

	void Update(){
		if (!gameOver) {
			if (numColorsFilled == 4 && !CheckGameWin ()) {
				if (numRows == 8) {
					GameOver ("You Lose :(");
				} else {
					startPos_Y += 80;
					RemoveInteractablityFromCircleRow ();
					BuildGameCircleRow ();
					numColorsFilled = 0;
				}
			}
		}
	}

	public int ColorsFilled{
		get{ return numColorsFilled; }
		set{ numColorsFilled = value; }
	}

	public Sprite WhiteCircle{
		get{ return whiteCircle; }
	}

	private void BuildSecretCode(){
		for (int i = 0; i < secretCodeObjects.Length; i++) {
			int randNum = Random.Range (0, colorSprites.Length);
			secretCodeObjects[i].GetComponent<Image>().sprite = colorSprites[randNum];
		}
	}

	private void BuildGameCircleRow(){
		gameCircleArray = new GameObject[rowLength];
		float x_pos = startPos_X;
		float y_pos = startPos_Y;
		for (int i = 0; i < rowLength; i++) {
			GameObject circle = Instantiate (gameCircle, Vector3.zero, Quaternion.identity);
			circle.transform.SetParent (this.canvas.transform);
			circle.GetComponent<ClickGameBoardCircle> ().setStateCircle = stateCircle;
			circle.GetComponent<ClickGameBoardCircle> ().setGameController = this;

			Vector3 localPos = circle.GetComponent<RectTransform> ().localPosition;
			localPos.x = x_pos;
			circle.GetComponent<RectTransform> ().localPosition = localPos;

			Vector3 pos = circle.GetComponent<RectTransform> ().position;
			pos.y = y_pos;
			circle.GetComponent<RectTransform>().position = pos;

			gameCircleArray [i] = circle;
			x_pos += 78.0f;
		}
		numRows++;
	}

	private void RemoveInteractablityFromCircleRow(){
		for (int i = 0; i < rowLength; i++) {
			gameCircleArray [i].GetComponent<Button> ().enabled = false;
		}
	}

	private void createFeedBackCircles(){
		Sprite[] feedBackColors = new Sprite[rowLength];
		Sprite[] tempSecretColors = new Sprite[rowLength];
		for (int i = 0; i < rowLength; i++) {
			if (gameCircleArray [i].GetComponent<Image> ().sprite == secretCodeObjects [i].GetComponent<Image> ().sprite) {
				feedBackColors [i] = redCircle;
			} else {
				feedBackColors [i] = null;
			}
			tempSecretColors[i] = secretCodeObjects[i].GetComponent<Image> ().sprite;
		}

		for (int i = 0; i < rowLength; i++) {
			for (int j = 0; j < rowLength; j++) {
				if ((gameCircleArray [i].GetComponent<Image> ().sprite == tempSecretColors [j]) && feedBackColors[i] != redCircle && feedBackColors[j] != redCircle) {
					feedBackColors [i] = whiteCircle;
					tempSecretColors [j] = null;
				}
			}
		}

		for (int i = 0; i < rowLength; i++) {
			for(int j = i+1; j < rowLength; j++){
				if (feedBackColors [j] == redCircle) {
					Sprite temp = feedBackColors [i];
					feedBackColors [i] = feedBackColors [j];
					feedBackColors [j] = temp;
				}
			}
		}

		for (int i = 0; i < rowLength; i++) {
			if (feedBackColors [i] != redCircle) {
				for (int j = i + 1; j < rowLength; j++) {
					if (feedBackColors [j] == whiteCircle) {
						Sprite temp = feedBackColors [i];
						feedBackColors [i] = feedBackColors [j];
						feedBackColors [j] = temp;
					}
				}
			}
		}

		float x_pos = (4 * 78.0f) + startPos_X;
		float y_pos = startPos_Y;
		for (int i = 0; i < rowLength; i++) {
			if (feedBackColors [i] != null) {
				GameObject circle = Instantiate (gameCircle, Vector3.zero, Quaternion.identity);
				circle.transform.SetParent (this.canvas.transform);
				circle.GetComponent<ClickGameBoardCircle> ().setStateCircle = stateCircle;
				circle.GetComponent<ClickGameBoardCircle> ().setGameController = this;

				circle.GetComponent<Button> ().enabled = false;
				circle.GetComponent<Image> ().sprite = feedBackColors [i];
				circle.transform.localScale = new Vector3 (0.5f, 0.5f, 1.0f);

				Vector3 localPos = circle.GetComponent<RectTransform> ().localPosition;
				localPos.x = x_pos;
				circle.GetComponent<RectTransform> ().localPosition = localPos;

				Vector3 pos = circle.GetComponent<RectTransform> ().position;
				pos.y = y_pos;
				circle.GetComponent<RectTransform> ().position = pos;

				x_pos += 39.0f;
			}
			if ((((i+1) % 2) == 0)) {
				y_pos += 39.0f;
				x_pos = (4 * 78.0f) + startPos_X;
			}
		}
	}

	private bool CheckGameWin(){
		createFeedBackCircles ();
		for (int i = 0; i < rowLength; i++) {
			if (gameCircleArray [i].GetComponent<Image> ().sprite != secretCodeObjects [i].GetComponent<Image> ().sprite) {
				return false;
			}
		}
		GameOver ("You Win! :)");
		return true;
	}

	private void GameOver(string gameOverText){
		gameOver = true;
		RemoveInteractablityFromCircleRow ();
		hintCircle.GetComponent<ClickGameBoardCircle> ().NoHints ();
		hintArray.SetActive (false);
		gameText.GetComponent<Text>().text = gameOverText;
		gameText.SetActive (true);
	}


}
