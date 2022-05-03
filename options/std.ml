
type algebra_solver =
  | Singular
  | Sage
  | Magma
  | Mathematica
  | Macaulay2
  | Maple
  | SMTSolver of string

type variable_order =
  | LexOrder
  | AppearingOrder
  | RevLexOrder
  | RevAppearingOrder

let default_range_solver = "boolector"

let default_algebra_solver = Singular

let z3_path = ref "z3"
let boolector_path = ref "boolector"
let mathsat_path = ref "mathsat"
let stp_path = ref "stp"
let minisat_path = ref "minisat"
let cryptominisat_path = ref "cryptominisat5"

let range_solver = ref default_range_solver
let range_solver_args = ref ""

let use_btor = ref false

let singular_path = ref "Singular"
let sage_path = ref "sage"
let magma_path = ref "magma"
let mathematica_path = ref "wolframscript"
let macaulay2_path = ref "M2"
let maple_path = ref "maple"

let algebra_solver = ref default_algebra_solver
let algebra_solver_args = ref ""
let string_of_algebra_solver s =
  match s with
  | Singular -> "singular"
  | Magma -> "magma"
  | Sage -> "sage"
  | Mathematica -> "mathematica"
  | Macaulay2 -> "macaulay2"
  | Maple -> "maple"
  | SMTSolver solver -> "smt:" ^ solver

let apply_rewriting = ref true
let polys_rewrite_replace_eexp = ref false
let apply_slicing = ref false

let variable_ordering = ref RevAppearingOrder
let string_of_variable_ordering o =
  match o with
  | LexOrder -> "lex"
  | AppearingOrder -> "appearing"
  | RevLexOrder -> "rev_lex"
  | RevAppearingOrder -> "rev_appearing"
let parse_variable_ordering str =
  if str = "lex" then LexOrder
  else if str = "appearing" then AppearingOrder
  else if str = "rev_lex" then RevLexOrder
  else if str = "rev_appearing" then RevAppearingOrder
  else raise Not_found

let verify_program_safety = ref true
let verify_epost = ref true
let verify_rpost = ref true
let verify_eassertion = ref true
let verify_rassertion = ref true
let verify_ecuts = ref None
let verify_rcuts = ref None
let verify_eacuts = ref None
let verify_racuts = ref None
let verify_scuts = ref None
let incremental_safety = ref false
let incremental_safety_timeout = ref 300

let carry_constraint = ref true

let verbose = ref false

let unix cmd =
  let r = Unix.system cmd in
  if r = r then ()
  else ()

let logfile = ref "cryptoline.log"

let trace msg =
  let ch = open_out_gen [Open_append; Open_creat; Open_text] 0o640 !logfile in
  let _ = output_string ch msg in
  let _ = output_string ch "\n" in
  let _ = close_out ch in
  ()

let fail s = trace s; failwith s

let string_of_running_time st ed = (Printf.sprintf "%f" (ed -. st)) ^ " seconds"

let vprint msg = if !verbose then print_string msg; flush stdout

let vprintln msg = if !verbose then print_endline msg; flush stdout

let jobs = ref 4

let use_cli = ref false

let cli_path = ref "cv_cli"

let rename_local = ref false

let auto_cast = ref false
let auto_cast_preserve_value = ref false
let typing_file = ref None
let use_binary_repr = ref false

let keep_temp_files = ref false
let tmpdir = ref None
let tmpfile prefix suffix =
  match !tmpdir with
  | None -> Filename.temp_file prefix suffix
  | Some dir -> Filename.temp_file ~temp_dir:dir prefix suffix
let cleanup files =
  if not !keep_temp_files then List.iter Unix.unlink files

let cryptoline_filename_extension = ".cl"

let native_smtlib_expn_operator = ref None

let two_phase_rewriting = ref true
