(define (problem blocks-tower)
  (:domain BLOCKS)
  (:objects
    a - block
    b - block
    c - block
    d - block
  )
  (:init
    (ontable a)
    (clear a)
    (ontable b)
    (clear b)
    (ontable c)
    (clear c)
    (ontable d)
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
