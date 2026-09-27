(define (problem blocks-problem)
  (:domain BLOCKS)
  (:objects
    a - block
    b - block
    c - block
    d - block
  )
  (:init
    (on c b)
    (clear c)
    (clear b)
    (ontable a)
    (clear a)
    (ontable d)
    (clear d)
    (handempty)
  )
  (:goal
    (and
      (on a b)
      (on b c)
      (on c d)
    )
  )
)
