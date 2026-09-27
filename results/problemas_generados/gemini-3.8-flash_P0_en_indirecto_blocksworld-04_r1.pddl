(define (problem blocks-4-tower)
  (:domain BLOCKS)
  (:objects
    a b c d - block
  )
  (:init
    (handempty)
    (ontable a)
    (ontable b)
    (ontable c)
    (ontable d)
    (clear a)
    (clear b)
    (clear c)
    (clear d)
  )
  (:goal
    (and
      (on d c)
      (on c b)
      (on b a)
    )
  )
)
