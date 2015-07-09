﻿using System;
using System.Collections.Generic;
namespace BizHawk.Client.EmuHawk
{
	public partial class TAStudio : IControlMainform
	{
		private bool _suppressAskSave = false;
		private bool _alreadyRewinding = false;

		public bool WantsToControlReadOnly { get { return false; } }
		public void ToggleReadOnly()
		{
			GlobalWin.OSD.AddMessage("TAStudio does not allow manual readonly toggle");
		}

		public bool WantsToControlStopMovie { get; private set; }

		public void StopMovie(bool supressSave)
		{
			this.Focus();
			_suppressAskSave = supressSave;
			NewTasMenuItem_Click(null, null);
			_suppressAskSave = false;
		}

		public bool WantsToControlRewind { get { return true; } }

		public void CaptureRewind()
		{
			// Do nothing, Tastudio handles this just fine
		}

		public bool Rewind()
		{
			if (_alreadyRewinding == false)
			{
				// We may have gotten here from Rewind in StepRunLoop_Core
				// we want to turn off the rewind control to prevent unintentional recursion
				_alreadyRewinding = true;
				GoToPreviousFrame();
				_alreadyRewinding = false;
			}
			return true;
		}

		public bool WantsToControlRestartMovie { get; private set; }

		public void RestartMovie()
		{
			if (AskSaveChanges())
			{
				WantsToControlStopMovie = false;
				StartNewMovieWrapper(false);
				WantsToControlStopMovie = true;
				RefreshDialog();
			}
		}
	}
}
