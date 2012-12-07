﻿using Bumblebee.Interfaces.Conditional;
using OpenQA.Selenium;

namespace Bumblebee.Implementation.Conditional
{
    public class ConditionalClickable : Element, IConditionalClickable
    {
        public ConditionalClickable(Block parent, By by)
            : base(parent, by)
        {
        }

        public ConditionalClickable(Block parent, IWebElement element)
            : base(parent, element)
        {
        }

        public TResult Click<TResult>() where TResult : Block
        {
            Tag.Click();
            return Session.CurrentBlock<TResult>(ParentElement);
        }

        public AlertDialog ClickExpectingAlert()
        {
            Tag.Click();
            return new AlertDialog(ParentElement, Session);
        }
    }
}
