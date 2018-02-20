using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class ClickGameBoardCircle : MonoBehaviour {
	[SerializeField]
	private GameObject stateCircle;
	[SerializeField]
	private GameController gameController;
	[SerializeField]
	private GameObject[] hintArray = new GameObject[4];
	private int hintCount = 0;
	private bool isFilled = false;
	private Sprite whiteCircle;

	void Start(){
		whiteCircle = gameController.WhiteCircle;
	}

	public GameObject setStateCircle{
		set{ stateCircle = value; }
	}

	public GameController setGameController{
		set{ gameController = value; }
	}

	public void ClickedPaletteColor(){
		stateCircle.GetComponent<Image> ().sprite = gameObject.GetComponent<Image> ().sprite;
	}

	public void ClickedGameCircle(){
		if (stateCircle.GetComponent<Image> ().sprite != whiteCircle) {
			gameObject.GetComponent<Image> ().sprite = stateCircle.GetComponent<Image> ().sprite;
			if (!isFilled) {
				gameController.ColorsFilled++;
				isFilled = true;
			}
		}
	}

	public void Hint(){
		if (hintCount < hintArray.Length) {
			hintArray [hintCount].SetActive (false);
			hintCount++;
		}
		if (hintCount == hintArray.Length) {
			NoHints ();
		}
	}

	public void NoHints(){
		gameObject.GetComponent<Button>().enabled = false;
	}

	public void Exit(){
		Application.Quit ();
		SceneManager.LoadScene (0);
	}
}
