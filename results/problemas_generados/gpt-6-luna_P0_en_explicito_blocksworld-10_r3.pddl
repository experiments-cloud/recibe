(define (problem blocks-problem)
  (:domain BLOCKS)
  (:objects
    a - block
    b - block
    c - block
    d - block
    e - block
    f - block
    g - block
    h - block
  )
  (:init
    (ontable b)
    (ontable c)
    (ontable e)
    (ontable f)
    (on a g)
    (on d h)
    (on g e)
    (on h f)
    (clear a)
    (clear b)
    (clear c)
    (clear d)
    (handempty)
  )
  (:goal
    (and
      (on a g)
      (on c a)
      (on d f)
      (on e h)
      (on f e)
      (on g b)
      (on h c)
    )
  )
)
