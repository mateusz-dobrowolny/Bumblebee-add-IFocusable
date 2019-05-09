﻿using System.Collections.Generic;

namespace Bumblebee.Interfaces
{
	public interface IRadioButtons<out TResult> : IFocusable<TResult> where TResult : IBlock
	{
		IEnumerable<IOption<TResult>> Options { get; }
	}
}