// Compiled with:
//    ~/Downloads/flex_sdk/bin/mxmlc -static-link-runtime-shared-libraries -debug -default-size 300 300 -default-frame-rate 15 testcase.as -o testcase.swf && rsync -Pav testcase.swf people:public_html

package {
	import flash.display.Sprite;
	import flash.net.URLRequest;
	import flash.display.Loader;
	import flash.display.LoaderInfo;
	import flash.events.Event;
	import flash.events.ProgressEvent;
	import flash.events.HTTPStatusEvent;
	import flash.events.IOErrorEvent;

	public class testcase extends Sprite {
		public function testcase()
		{
			trace(1);
	
			var url:String = "http://www.buck-3.dev.yelp.com/html/flash/swfupload.swf";
			var req:URLRequest = new URLRequest(url);
			var myLoader:Loader = new Loader();

			trace(2);
			myLoader.contentLoaderInfo.addEventListener(Event.COMPLETE, onCompleteHandler);
			trace(3);
			myLoader.contentLoaderInfo.addEventListener(ProgressEvent.PROGRESS, onProgressHandler);
			myLoader.contentLoaderInfo.addEventListener(HTTPStatusEvent.HTTP_STATUS, onHttpStatus);
			myLoader.contentLoaderInfo.addEventListener(Event.INIT, onInit);
			myLoader.contentLoaderInfo.addEventListener(IOErrorEvent.IO_ERROR, onIoError);
			myLoader.contentLoaderInfo.addEventListener(Event.OPEN, onOpen);
			myLoader.contentLoaderInfo.addEventListener(Event.UNLOAD, onUnload);
			trace(4);
			myLoader.load(req)
			trace(5);
		}

		public function onCompleteHandler(loadEvent:Event):void
		{
			trace(7);
			var target:LoaderInfo = (LoaderInfo)(loadEvent.currentTarget);
			trace(8);
			trace('TARGET', target);
			var data = target.content;
			trace(9);
			trace(data);
			var build_number = data.build_number;
			trace(10);
			trace(build_number);
		}

		public function onProgressHandler(mProgress:ProgressEvent):void
		{
			trace(6);
			var percent:Number = mProgress.bytesLoaded/mProgress.bytesTotal;
			trace(percent * 100 + "%");
		}

		public function onHttpStatus(mProgress:HTTPStatusEvent):void
		{
			trace("EVENT: http status")
		}
		public function onInit(mProgress:Event):void
		{
			trace("EVENT: init")
		}
		public function onIoError(mProgress:IOErrorEvent):void
		{
			trace("EVENT: io errro")
		}
		public function onOpen(mProgress:Event):void
		{
			trace("EVENT: open")
		}
		public function onUnload(mProgress:Event):void
		{
			trace("EVENT: unload")
		}
	}
}
