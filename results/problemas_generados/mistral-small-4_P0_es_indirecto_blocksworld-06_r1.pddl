(define (problem BLOCKS-PROBLEM)
  (:domain BLOCKS)
  (:objects
    a b c d e f - block
  )
  (:init
    (on f e)
    (on e b)
    (ontable b)
    (on d a)
    (on a c)
    (ontable c)
    (handempty)
    (clear f)
    (clear d)
  )
  (:goal (and
    (on c b)
    (on b a)
    (on a e)
    (on e f)
    (on f d)
  ))
)
