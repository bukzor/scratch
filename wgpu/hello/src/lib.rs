use winit::{
    event::{ElementState, Event, KeyboardInput, VirtualKeyCode, WindowEvent},
    //event::*,
    event_loop::{ControlFlow, EventLoop},
    window::{Window, WindowBuilder},
};

pub fn run() -> Result<(), winit::error::OsError> {
    // https://sotrh.github.io/learn-wgpu/beginner/tutorial1-window/#env-logger
    env_logger::init();
    println!("Hello, world!");

    let event_loop = EventLoop::new();
    let window = WindowBuilder::new().build(&event_loop)?;

    event_loop.run(make_event_handler(window))
}

pub fn make_event_handler<T>(window: Window) -> impl Fn(Event<()>, &T, &mut ControlFlow) {
    move |event, _, control_flow| match event {
        Event::WindowEvent { window_id, event } => {
            if window_id == window.id() {
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
        Event::NewEvents(cause) => println!("new events: {cause:?}"),
        Event::Resumed => println!("Resumed!"),
        Event::MainEventsCleared => println!("main events cleared"),
        Event::RedrawRequested(winid) => println!("Redraw requested: {winid:?}"),
        Event::RedrawEventsCleared => println!("redraw events cleared"),
        Event::DeviceEvent { .. } => todo!(),
        Event::UserEvent(_) => todo!(),
        Event::Suspended => todo!(),
        Event::LoopDestroyed => todo!(),
    }
}
