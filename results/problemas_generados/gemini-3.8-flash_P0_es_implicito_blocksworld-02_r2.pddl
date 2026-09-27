(define (problem blocks-problem)
  (:domain BLOCKS)
  (:objects
    a - block
    b - block
    c - block
    d - block
  )
  (:init
    (handempty)
    (ontable a)
    (clear a)
    (ontable d)
    (clear d)
    (ontable b)
    (on c b)
    (clear c)
  )
  (:goal
    (and
      (on a b)
      (on b c)
      (on c d)
    )
  )
)
