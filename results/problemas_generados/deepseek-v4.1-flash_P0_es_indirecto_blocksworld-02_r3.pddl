(define (problem blocks-tower)
  (:domain BLOCKS)
  (:objects
    a b c d - block
  )
  (:init
    (ontable a)
    (ontable b)
    (ontable d)
    (clear a)
    (clear c)
    (clear d)
    (on c b)
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
