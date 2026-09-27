(define (problem blocks-tower)
  (:domain BLOCKS)
  (:objects
    a b c d - block
  )
  (:init
    (handempty)
    (on c b)
    (ontable b)
    (ontable a)
    (ontable d)
    (clear c)
    (clear a)
    (clear d)
  )
  (:goal
    (and
      (on a b)
      (on b c)
      (on c d)
    )
  )
)
