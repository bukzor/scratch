module Main where
import System.Environment

f x y z = x ^ y

main :: IO ()
main = do
  (a : b : c : _) <- getArgs
  let n = read a :: Integer
  let m = read b :: Integer
  let k = read c :: Integer
  putStrLn $ show $ filter even $ map (f n m) [0..k]
