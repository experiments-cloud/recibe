(define (problem blocks-problem)
  (:domain BLOCKS)
  (:objects
    a b c d e f - block
  )
  (:init
    (on e b)
    (on f e)
    (clear f)
    (ontable b)
    (on a c)
    (on d a)
    (clear d)
    (ontable c)
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
