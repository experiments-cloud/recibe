(define (problem blocks-problem)
  (:domain BLOCKS)
  (:objects
    a b c d e f - block
  )
  (:init
    (handempty)
    (ontable b)
    (on e b)
    (on f e)
    (clear f)
    (ontable c)
    (on a c)
    (on d a)
    (clear d)
  )
  (:goal
    (and
      (on c b)
      (on b a)
      (on a e)
      (on e f)
      (on f d)
    )
  )
)
