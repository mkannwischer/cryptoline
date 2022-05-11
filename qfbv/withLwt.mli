
(** This module provides functions that solve QF_BV queries concurrently with Lwt. *)

open Common

val solve_simp : ?timeout:int -> ?header:(string list) -> bexp list -> result Lwt.t
(** [solve_simp ~timeout:t ~header:ss [e1; e2; ...; en]] verifies if e{_ n} is implied by the conjunction of e{_ 1}, ..., and e{_ n-1}. *)
