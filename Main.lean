import GameServer.Server
import NNG.NNG

def System.FilePath.parent! (fp : System.FilePath) : System.FilePath :=
  match fp.parent with
  | some path => path
  | none => panic! "Couldn't find parent folder"

unsafe def main : IO Unit := do
  let build_folder := (← IO.appPath).parent!.parent!
  -- TODO: Find a way to build this list properly
  -- the second item in the list is especially horrible: it assumes game-server is in the same folder as nng4
  let paths : List System.FilePath := [build_folder/"lib", 
                                       build_folder.parent!.parent!/"game-server"/"build"/"lib",
                                       (← Lean.findSysroot) / "lib" / "lean"]
  Server.runGame `NNG paths
