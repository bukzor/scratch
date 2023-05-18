#![allow(unused_imports)] // FIXME: delete me
#![allow(dead_code)] // FIXME: delete me
#![allow(unused_variables)] // FIXME: delete me

use winit::{
    event::{ElementState, Event, KeyboardInput, VirtualKeyCode, WindowEvent},
    //event::*,
    event_loop::{ControlFlow, EventLoop},
    window::{Window, WindowBuilder},
};

//type Result<T> = std::error::Result;
type Error = Box<dyn std::error::Error>;
pub type Result<T> = core::result::Result<T, Error>;

fn main() -> Result<()> {
    // https://sotrh.github.io/learn-wgpu/beginner/tutorial1-window/#env-logger
    env_logger::init();
    println!("Hello, world!");

    let event_loop = EventLoop::new();
    let window = WindowBuilder::new().build(&event_loop)?;

    let handler = Handler { window };
    event_loop.run(move |a, b, c| handler.call(a, b, c))
}

struct Handler {
    window: Window,
}

impl Handler {
    fn call<T>(&self, event: Event<()>, _: &T, control_flow: &mut ControlFlow) {
        match event {
            Event::WindowEvent { window_id, event } => {
                if window_id == self.window.id() {
                    match event {
                        WindowEvent::CloseRequested
                        | WindowEvent::KeyboardInput {
                            input:
                                KeyboardInput {
                                    state: ElementState::Pressed,
                                    virtual_keycode: Some(VirtualKeyCode::Escape),
                                    ..
                                },
                            ..
                        } => *control_flow = ControlFlow::Exit,
                        _ => {}
                    }
                }
            }
            Event::NewEvents(_) => todo!(),
            Event::DeviceEvent { device_id, event } => todo!(),
            Event::UserEvent(_) => todo!(),
            Event::Suspended => todo!(),
            Event::Resumed => todo!(),
            Event::MainEventsCleared => todo!(),
            Event::RedrawRequested(_) => todo!(),
            Event::RedrawEventsCleared => todo!(),
            Event::LoopDestroyed => todo!(),
        }
    }
}
