(define (problem blocks-torre)
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
      (on d c)
      (on c b)
      (on b a)
    )
  )
)
