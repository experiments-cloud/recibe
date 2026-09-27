(define (problem blocks-problem)
  (:domain BLOCKS)
  (:objects
    a - block
    b - block
    c - block
    d - block
  )
  (:init
    (ontable a)
    (ontable b)
    (ontable c)
    (ontable d)
    (clear a)
    (clear b)
    (clear c)
    (clear d)
    (handempty)
  )
  (:goal
    (and
      (on b a)
      (on c b)
      (on d c)
    )
  )
)
