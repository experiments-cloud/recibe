(define (problem blocks-problem)
  (:domain BLOCKS)
  (:objects
    a b c d e f - block
  )
  (:init
    (on e b)
    (on f e)
    (ontable b)
    (clear f)
    (on a c)
    (on d a)
    (ontable c)
    (clear d)
    (handempty)
  )
  (:goal (and
    (on c b)
    (on b a)
    (on a e)
    (on e f)
    (on f d)
  ))
)
