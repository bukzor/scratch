//type Result<T> = std::error::Result;
type Error = Box<dyn std::error::Error>;
pub type Result<T> = core::result::Result<T, Error>;

fn main() -> Result<()> {
    use hello::*;
    run()
}
